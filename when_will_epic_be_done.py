import argparse
import base64
import requests
from datetime import datetime, timedelta

# Dictionary mapping human-readable field names to corresponding Jira field identifiers
# This mapping allows for easier reference to Jira field identifiers based on their human-readable names.
JIRA_FIELD_NAMES = {
    "Key": "key",
    "Summary": "summary",
    "Status": "status",
    "Story Points": "customfield_10023"  # Adjust field ID and name accordingly
}


def show_custom_fields():
    """Call this to dump all the custom fields"""
    response = requests.get(args.base_url + "field", headers=HEADERS)

    if response.status_code == 200:
        fields = response.json()
        custom_fields = [field for field in fields if field['custom']]
        for custom_field in custom_fields:
            print(custom_field['id'], "-", custom_field['name'])
    else:
        print(f"Failed to retrieve custom fields. Status code: {response.status_code}")


def get_stories_from_epic(epic_key):
    """Retrieve all stories associated with the given epic."""
    jql_query = f'"Epic Link" = {epic_key}'
    search_url = args.base_url + "search"

    # Construct fields parameter using FIELD_NAMES dictionary
    fields_param = ",".join(JIRA_FIELD_NAMES.values())

    response = requests.get(search_url, headers=HEADERS, params={"jql": jql_query,
                                                                 "fields": fields_param})
    if response.status_code != 200:
        print(f"Failed to fetch stories for epic {epic_key}. Status code: {response.status_code}")
        return []

    stories = response.json()["issues"]
    return stories


if __name__ == "__main__":
    # Argument parser for command line usage
    parser = argparse.ArgumentParser(
        description='Tally up the total story points of user stories in a Jira epic and project completion dates.')
    parser.add_argument('epic', help='Jira epic ticket name, e.g., ABC-1234')
    parser.add_argument('--story-points-per-sprint', type=int, default=13,
                        help='Number of story points a developer can finish in a 2-week Agile Sprint.')
    parser.add_argument('--max-developers', type=int, default=1, help='Maximum number of developers.')
    parser.add_argument('--exclude', nargs='+', default=[],
                        help='List of Jira tickets to exclude from the calculations, e.g., ABC-5678 ABC-5679')
    parser.add_argument('--base-url', required=True,
                        help='Base URL for Jira API')
    parser.add_argument('--browse-url', required=True,
                        help='Base URL for Jira browse links')
    parser.add_argument('--email', help='Jira account email')
    parser.add_argument('--api-token', help='Jira API token')
    parser.add_argument('--sprint-duration', type=int, default=14, nargs='?',
                        help='Duration of Agile Sprint in days')

    args = parser.parse_args()

    # Headers for API authentication
    HEADERS = {
        "Authorization": f"Basic {base64.b64encode(f'{args.email}:{args.api_token}'.encode()).decode()}",
        "Content-Type": "application/json",
    }

    # Fetch stories from the given epic
    stories = get_stories_from_epic(args.epic)

    total_story_points = 0

    # Display header
    epic_link = f"{args.browse_url}{args.epic}"
    print()
    print(f"Child Issues within the Epic: {args.epic} {epic_link}")
    print(f"{'Key':<15}{'Summary':<60}{'Status':<25}{'Story Points':<15}{'Link'}")

    open_story_points = 0  # This will hold the sum of story points for tickets not in "Closed" status

    # Loop through each story and display details, skip stories in the exclude list
    for story in stories:
        key = story["key"]

        summary = story["fields"].get("summary", "")
        status = story["fields"]["status"]["name"]
        story_points_field = JIRA_FIELD_NAMES["Story Points"]
        story_points = story["fields"].get(story_points_field, 0)  # Adjust field id to your story points field id
        link = f"{args.browse_url}{key}"
        print(f"{key:<15}{summary[:57]:<60}{status:<25}{story_points:<15}{link}")

        if story_points:
            total_story_points += story_points

        # Skip if the story is in the exclude list
        if key in args.exclude:
            continue

        if status != "Closed" and story_points:
            open_story_points += story_points

    # Display total story points and project end dates
    print(f"\nTotal story points for epic {args.epic}: {total_story_points}")
    print(f"Total story points for tickets that are not 'Closed' and not excluded: {open_story_points}")
    print()
    print(f"Excluded tickets: {args.exclude}")
    print()
    print("WHEN WILL IT BE DONE?????")
    print(f"=" * 80)
    print(f"Given that 1 developer can finish {args.story_points_per_sprint} story points in a 2-week Agile Sprint:")
    for devs in range(1, args.max_developers + 1):
        sprints_required = open_story_points / (args.story_points_per_sprint * devs)
        total_days_required = sprints_required * args.sprint_duration
        end_date = datetime.now() + timedelta(days=total_days_required)
        print(f"Projected end date with {devs} developer(s): {end_date.strftime('%Y-%m-%d')}")
