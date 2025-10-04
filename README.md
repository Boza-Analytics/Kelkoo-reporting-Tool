# Kelkoo API to Google Sheets - Documentation

## Overview
This Python script fetches campaign statistics from the Kelkoo API and automatically exports the data to Google Sheets. It runs weekly reports showing campaign costs, clicks, and budget utilization for multiple advertising accounts.

---

## Table of Contents

1. [Requirements](#requirements)
2. [Configuration](#configuration)
3. [Features](#features)
4. [Script Workflow](#script-workflow)
5. [Functions Reference](#functions-reference)
6. [Google Sheets Integration](#google-sheets-integration)
7. [Date Calculations](#date-calculations)
8. [Error Handling](#error-handling)
9. [Customization](#customization)

---

## Requirements

### Python Packages
```bash
pip install requests gspread oauth2client
```

**Required Libraries:**
- `requests` - HTTP requests to Kelkoo API
- `gspread` - Google Sheets API wrapper
- `oauth2client` - Google OAuth authentication
- `datetime` - Date/time calculations

### API Access
- **Kelkoo API Access**: Valid JWT tokens for each account
- **Google Cloud Platform**: Service account with Google Sheets API enabled
- **Google Sheets**: Spreadsheet with appropriate sharing permissions

---

## Configuration

### API Settings

```python
BASE_URL = "https://api.kelkoogroup.net/merchant/statistics/v1"
JWT_TOKEN1 = ""  # First account JWT token
JWT_TOKEN2 = ""  # Second account JWT token
GOOGLE_SHEET_KEY = ""  # Google Sheet ID from URL
```

### Campaign IDs

Define your campaigns for each account:

```python
CAMPAIGN_IDS1 = {
    "Campaign Name 1": "campaign_id_1",
    "Campaign Name 2": "campaign_id_2",
    # Add more campaigns
}

CAMPAIGN_IDS2 = {
    "Campaign Name A": "campaign_id_a",
    "Campaign Name B": "campaign_id_b",
    # Add more campaigns
}
```

### Monthly Budgets

Set budget limits in the `get_monthly_budget()` function:

```python
def get_monthly_budget(campaign_name):
    monthly_budgets = {
        "Campaign Name 1": 5000,  # Budget in your currency
        "Campaign Name 2": 3000,
        # Add more budgets
    }
    return monthly_budgets.get(campaign_name, 0)
```

### Google Service Account

**Required File:** Service account JSON key
- **Path**: `C:/Users/info/Desktop/Python/KEYS/gcp-b-409518-c59fbac920ba.json`
- **Update** this path to match your file location

---

## Features

### 1. Multi-Account Support
- Processes multiple Kelkoo accounts sequentially
- Separate JWT tokens for each account
- Consolidated reporting in single spreadsheet

### 2. Automatic Date Range
- Calculates previous week (Monday to Sunday)
- Dynamic date calculation based on current date
- No manual date entry required

### 3. Budget Tracking
- Calculates percentage of monthly budget used
- Per-campaign budget monitoring
- Customizable budget thresholds

### 4. Organized Data Storage
- Creates new worksheet for each run
- Timestamped worksheet names
- Preserves historical data

### 5. Category-Level Statistics
- Total cost per campaign
- Total clicks per campaign
- Currency information
- Budget utilization percentage

---

## Script Workflow

### Execution Flow

```
1. Calculate Date Range
   ↓
2. Create Timestamp
   ↓
3. Authenticate with Google Sheets
   ↓
4. Process Account 1
   ├─ For each campaign:
   │  ├─ Fetch category data
   │  ├─ Calculate totals
   │  ├─ Calculate budget %
   │  └─ Insert into sheet
   ↓
5. Process Account 2
   ├─ (Same as Account 1)
   ↓
6. Complete
```

---

## Functions Reference

### `get_jwt_headers(jwt_token)`
Creates authorization headers for API requests.

**Parameters:**
- `jwt_token` (str): JWT authentication token

**Returns:**
- `dict`: Headers with Bearer token and content type

**Example:**
```python
headers = get_jwt_headers("your_jwt_token")
# Returns: {"Authorization": "Bearer your_jwt_token", "Content-Type": "application/json"}
```

---

### `get_campaigns(jwt_token)`
Fetches all available campaigns for an account.

**Parameters:**
- `jwt_token` (str): JWT authentication token

**Returns:**
- `dict`: JSON response with campaign data

**API Endpoint:** `GET /my-campaigns`

**Note:** Currently defined but not used in main workflow

---

### `get_category_data(jwt_token, campaign_id, start_date, end_date)`
Retrieves category statistics for a specific campaign.

**Parameters:**
- `jwt_token` (str): JWT authentication token
- `campaign_id` (str): Campaign identifier
- `start_date` (str): Start date (YYYY-MM-DD)
- `end_date` (str): End date (YYYY-MM-DD)

**Returns:**
- `list`: Array of category statistics

**API Endpoint:** `GET /category/{campaign_id}?startDate={start_date}&endDate={end_date}`

**Response Structure:**
```json
[
    {
        "cost": 123.45,
        "clicks": 67,
        "currency": "EUR"
    }
]
```

---

### `insert_data_into_google_sheet(sheet, campaign_name, total_cost, total_clicks, currency, timestamp, percentage_of_budget_used)`
Inserts campaign data into Google Sheets.

**Parameters:**
- `sheet` (gspread.Spreadsheet): Google Sheets object
- `campaign_name` (str): Name of the campaign
- `total_cost` (float): Total campaign cost
- `total_clicks` (int): Total clicks
- `currency` (str): Currency code
- `timestamp` (str): Run timestamp
- `percentage_of_budget_used` (float): Budget utilization %

**Behavior:**
- Creates new worksheet if it doesn't exist
- Adds header row on new worksheet
- Appends data row for each campaign

**Worksheet Header:**
```
Account Name | Total Cost | Total Clicks | Currency | % of Budget Used | Timestamp
```

---

### `get_monthly_budget(campaign_name)`
Returns the monthly budget for a campaign.

**Parameters:**
- `campaign_name` (str): Name of the campaign

**Returns:**
- `float`: Monthly budget amount (0 if not found)

**Usage:**
Define budgets in the function:
```python
monthly_budgets = {
    "Campaign A": 5000,
    "Campaign B": 3000
}
```

---

### `process_account(campaign_ids, jwt_token, sheet, start_date, end_date, timestamp)`
Processes all campaigns for a single account.

**Parameters:**
- `campaign_ids` (dict): Campaign name to ID mapping
- `jwt_token` (str): JWT authentication token
- `sheet` (gspread.Spreadsheet): Google Sheets object
- `start_date` (str): Report start date
- `end_date` (str): Report end date
- `timestamp` (str): Run timestamp

**Process:**
1. Iterates through all campaigns
2. Fetches category data from API
3. Calculates totals and budget percentage
4. Inserts data into Google Sheet

---

### `main()`
Main execution function.

**Workflow:**
1. Calculate date range (previous week)
2. Generate timestamp
3. Authenticate with Google Sheets
4. Process all accounts
5. Print confirmation messages

---

## Google Sheets Integration

### Authentication Setup

1. **Create Service Account:**
   - Go to Google Cloud Console
   - Create new project
   - Enable Google Sheets API
   - Create service account
   - Download JSON key

2. **Share Spreadsheet:**
   - Open your Google Sheet
   - Click "Share"
   - Add service account email
   - Grant "Editor" permissions

3. **Configure Script:**
```python
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    "path/to/your/service-account.json",
    scope
)
client = gspread.authorize(credentials)
sheet = client.open_by_key(GOOGLE_SHEET_KEY)
```

### Worksheet Naming

**Format:** `RUN_YYYYMMDDHHmmss_From_YYYY-MM-DD_To_YYYY-MM-DD`

**Example:** `RUN_20250104143022_From_2024-12-30_To_2025-01-05`

---

## Date Calculations

### Weekly Report Range

The script calculates the previous Monday to Sunday:

```python
# Get date 7 days ago
start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

# Calculate last Monday
last_monday = datetime.strptime(start_date, "%Y-%m-%d") - timedelta(days=datetime.now().weekday())

# Calculate next Sunday (6 days after Monday)
next_sunday = last_monday + timedelta(days=6)
```

### Example Calculation

**Today:** Thursday, January 4, 2025
- **Last Monday:** December 30, 2024
- **Next Sunday:** January 5, 2025
- **Report Range:** December 30 - January 5

---

## Error Handling

### API Errors

```python
response = requests.get(url, headers=get_jwt_headers(jwt_token))
if response.ok:
    return response.json()
else:
    response.raise_for_status()  # Raises HTTPError
```

**Common HTTP Errors:**
- `401 Unauthorized` - Invalid JWT token
- `404 Not Found` - Invalid campaign ID
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - API issue

### Google Sheets Errors

```python
try:
    worksheet = sheet.worksheet(f"RUN_{timestamp}")
except gspread.WorksheetNotFound:
    worksheet = sheet.add_worksheet(title=f"RUN_{timestamp}", rows="1000", cols="6")
```

**Common Issues:**
- Worksheet already exists (handled with try/except)
- Permission denied (check service account access)
- Quota exceeded (Google API limits)

---

## Customization

### Add More Accounts

```python
JWT_TOKEN3 = "your_third_token"
CAMPAIGN_IDS3 = {
    "Campaign Z": "campaign_id_z"
}

# In main():
process_account(CAMPAIGN_IDS3, JWT_TOKEN3, sheet, start_date, end_date, timestamp)
```

### Change Report Period

**Monthly Report:**
```python
from dateutil.relativedelta import relativedelta

start_date = (datetime.now() - relativedelta(months=1)).replace(day=1).strftime("%Y-%m-%d")
end_date = (datetime.now().replace(day=1) - timedelta(days=1)).strftime("%Y-%m-%d")
```

**Custom Date Range:**
```python
start_date = "2025-01-01"
end_date = "2025-01-31"
```

### Add More Columns

Modify `insert_data_into_google_sheet()`:

```python
# Update header
worksheet.append_row([
    "Account Name", 
    "Total Cost", 
    "Total Clicks", 
    "Currency", 
    "% of Budget Used", 
    "CPC",  # New column
    "Timestamp"
])

# Calculate CPC
cpc = total_cost / total_clicks if total_clicks > 0 else 0

# Update data row
worksheet.append_row([
    campaign_name, 
    total_cost, 
    total_clicks, 
    currency, 
    percentage_of_budget_used,
    cpc,  # New data
    timestamp
])
```

---

## Running the Script

### Command Line
```bash
python kelkoo_stats.py
```

### Scheduled Execution

**Windows Task Scheduler:**
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Weekly (Monday morning)
4. Action: Start a program
5. Program: `python.exe`
6. Arguments: `C:/path/to/kelkoo_stats.py`

**Linux Cron:**
```bash
# Run every Monday at 9 AM
0 9 * * 1 /usr/bin/python3 /path/to/kelkoo_stats.py
```

---

## Output Example

### Console Output
```
Start Date (Last Monday): 2024-12-30
End Date (Next Sunday): 2025-01-05
Timestamp: RUN_20250104143022_From_2024-12-30_To_2025-01-05
Processing Campaign: Campaign Name 1, ID: 12345...
Data inserted into Google Sheet for Campaign Name 1
Processing Campaign: Campaign Name 2, ID: 67890...
Data inserted into Google Sheet for Campaign Name 2
```

### Google Sheet Result
```
Account Name     | Total Cost | Total Clicks | Currency | % of Budget Used | Timestamp
Campaign Name 1  | 1234.56    | 789          | EUR      | 24.69           | RUN_20250104...
Campaign Name 2  | 567.89     | 234          | EUR      | 18.93           | RUN_20250104...
```

---

## Troubleshooting

### JWT Token Issues
- Tokens expire - regenerate from Kelkoo dashboard
- Check token format (no extra spaces)
- Verify account permissions

### Google Sheets Access
- Confirm service account email has editor access
- Check API quotas in Google Cloud Console
- Verify spreadsheet key is correct

### Date Calculation Issues
- Script uses system time - ensure correct timezone
- For specific date ranges, hardcode instead of calculating

---

## Security Best Practices

1. **Never commit credentials:**
   ```python
   # Use environment variables
   import os
   JWT_TOKEN1 = os.getenv('KELKOO_JWT_TOKEN1')
   ```

2. **Secure service account key:**
   - Store outside project directory
   - Restrict file permissions
   - Use secrets manager in production

3. **Validate API responses:**
   - Check for unexpected data structures
   - Handle missing fields gracefully
   - Log errors for monitoring

---

## License

Proprietary - For use with Kelkoo API integration only.

---

## Support

For issues:
1. Check console output for error messages
2. Verify API credentials are current
3. Test Google Sheets connection separately
4. Review Kelkoo API documentation for changes
