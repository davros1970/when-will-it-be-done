# Jira Epic Tracker

## Overview

This script is designed to assist project managers and development teams in tracking the progress of user stories within a Jira Epic. It calculates the total story points of user stories, excluding specified tickets, and provides projected completion dates based on the number of developers and their sprint velocity.

## Problem Statement

In Agile project management, tracking the progress of epics and estimating project completion dates can be challenging. This script aims to address this challenge by providing a tool that:

- Tally up the total story points of user stories within a Jira Epic.
- Exclude specific Jira tickets from the calculations.
- Project completion dates based on the number of developers and their sprint velocity.

## Why it's Needed

- **Efficient Project Planning:** This script allows project managers to quickly assess the status of an Epic, understand the total story points involved, and estimate completion dates based on team capacity.

- **Sprint Velocity Estimation:** By specifying the number of developers and their sprint velocity, the script provides insights into when the project is likely to be completed.

- **Customization:** Users can customize the script by excluding specific Jira tickets from the calculations, providing flexibility in handling unique project requirements.

## Usage

1. **Install Dependencies:**
   Ensure that you have the required dependencies installed. You can install them using the following:
   ```
   pip install requests
   ```

2. **Run the Script:**
   Execute the script by providing the necessary command-line arguments. Here's an example command:
   ```bash
   python script_name.py AV3-5769 --story-points-per-sprint 13 --max-developers 3 --exclude AV3-1234 AV3-5678 --base-url <JIRA_BASE_URL> --browse-url <JIRA_BROWSE_URL> --email <JIRA_EMAIL> --api-token <JIRA_API_TOKEN> --sprint-duration 14
   ```

   - `epic`: The Jira epic ticket name, e.g., AV3-5769.
   - `--story-points-per-sprint`: Number of story points a developer can finish in a 2-week Agile Sprint. Default is 13.
   - `--max-developers`: Maximum number of developers. Default is 1.
   - `--exclude`: List of Jira tickets to exclude from the calculations.
   - `--base-url`: Base URL for Jira API. Required.
   - `--browse-url`: Base URL for Jira browse links. Required.
   - `--email`: Jira account email.
   - `--api-token`: Jira API token.
   - `--sprint-duration`: Duration of Agile Sprint in days. Default is 14.

   - Replace `<JIRA_BASE_URL>`, `<JIRA_BROWSE_URL>`, `<JIRA_EMAIL>`, and `<JIRA_API_TOKEN>` with your Jira configuration.

3. **Review Output:**
   The script will output information about child issues within the specified Epic, including their key, summary, status, story points, and link. It will also provide total story points and projected completion dates based on the given parameters.

4. **Customization:**
   Customize the script further by adjusting parameters such as the number of developers, story points per sprint, and excluded tickets.

## Example Output

```
Child Issues within the Epic: ABC-1234 https://mycompany.atlassian.net/browse/AV3-5769
Key            Summary                                                        Status                  Story Points    Link
ABC-2222       Implement login functionality                                  In Progress             5               https://mycompany.atlassian.net/browse/ABC-2222
ABC-3333       Update user profile page                                       Closed                  3               https://mycompany.atlassian.net/browse/ABC-3333

Total story points for epic ABC-1234: 8
Total story points for tickets that are not 'Closed' and not excluded: 5

Excluded tickets: ['ABC-4444', 'ABC-5555']

WHEN WILL IT BE DONE?????
================================================================================
Given that 1 developer can finish 13 story points in a 2-week Agile Sprint:
Projected end date with 1 developer(s): 2024-03-08
Projected end date with 2 developer(s): 2024-03-05
Projected end date with 3 developer(s): 2024-03-04
```