import requests
from datetime import datetime, timedelta
import gspread
from oauth2client.service_account import ServiceAccountCredentials

BASE_URL = "https://api.kelkoogroup.net/merchant/statistics/v1"
JWT_TOKEN1 = ""
JWT_TOKEN2= ""
GOOGLE_SHEET_KEY = ""

CAMPAIGN_IDS1 = {

}

CAMPAIGN_IDS2 = {
  
}

def get_jwt_headers(jwt_token):
    return {"Authorization": f"Bearer {jwt_token}", "Content-Type": "application/json"}

def get_campaigns(jwt_token):
    url = f"{BASE_URL}/my-campaigns"
    response = requests.get(url, headers=get_jwt_headers(jwt_token))
    if response.ok:
        return response.json()
    else:
        response.raise_for_status()

def get_category_data(jwt_token, campaign_id, start_date, end_date):
    url = f"{BASE_URL}/category/{campaign_id}?startDate={start_date}&endDate={end_date}"
    response = requests.get(url, headers=get_jwt_headers(jwt_token))
    if response.ok:
        return response.json()
    else:
        response.raise_for_status()

def insert_data_into_google_sheet(sheet, campaign_name, total_cost, total_clicks, currency, timestamp, percentage_of_budget_used):
    try:
        worksheet = sheet.worksheet(f"RUN_{timestamp}")
    except gspread.WorksheetNotFound:
        worksheet = sheet.add_worksheet(title=f"RUN_{timestamp}", rows="1000", cols="6")
        worksheet.append_row(["Account Name", "Total Cost", "Total Clicks", "Currency", "% of Budget Used", "Timestamp"])

    worksheet.append_row([campaign_name, total_cost, total_clicks, currency, percentage_of_budget_used, timestamp])
    print(f"Data inserted into Google Sheet for {campaign_name}")

def get_monthly_budget(campaign_name):
    # Define monthly budgets for each campaign (you can adjust these values as needed)
    monthly_budgets = {
  
    }
    return monthly_budgets.get(campaign_name, 0)  # Return 0 if campaign not found

def process_account(campaign_ids, jwt_token, sheet, start_date, end_date, timestamp):
    for campaign_name, campaign_id in campaign_ids.items():
        print(f"Processing Campaign: {campaign_name}, ID: {campaign_id}...")
        category_data = get_category_data(jwt_token, campaign_id, start_date, end_date)

        total_cost = sum(item.get("cost", 0) for item in category_data)
        total_clicks = sum(item.get("clicks", 0) for item in category_data)
        currency = category_data[0].get("currency", "NAN") if category_data else "NAN"

        # Calculate monthly budget and percentage of budget used
        monthly_budget = get_monthly_budget(campaign_name)
        percentage_of_budget_used = (total_cost / monthly_budget) * 100 if monthly_budget != 0 else 0

        insert_data_into_google_sheet(sheet, campaign_name, total_cost, total_clicks, currency, timestamp, percentage_of_budget_used)

def main():
    # Get the start_date
    start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    
    # Calculate the date of last Monday
    last_monday = datetime.strptime(start_date, "%Y-%m-%d") - timedelta(days=datetime.now().weekday())
    
    # Calculate the date of next Sunday
    next_sunday = last_monday + timedelta(days=6)

    # Format the dates as strings
    last_monday_str = last_monday.strftime("%Y-%m-%d")
    next_sunday_str = next_sunday.strftime("%Y-%m-%d")  # Remove the time component

    # Use f-string to format the timestamp
    timestamp = f"RUN_{datetime.now().strftime('%Y%m%d%H%M%S')}_From_{last_monday_str}_To_{next_sunday_str}"
    
    print("Start Date (Last Monday):", last_monday_str)
    print("End Date (Next Sunday):", next_sunday_str)
    print("Timestamp:", timestamp)

    # Define end_date here
    end_date = next_sunday_str



    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name("C:/Users/info/Desktop/Python/KEYS/gcp-b-409518-c59fbac920ba.json", scope)
    client = gspread.authorize(credentials)
    sheet = client.open_by_key(GOOGLE_SHEET_KEY)

    # Format the timestamp to include the date selection
    timestamp = f"RUN_{datetime.now().strftime('%Y%m%d%H%M%S')}_From_{start_date}_To_{end_date}"

    process_account(CAMPAIGN_IDS1, JWT_TOKEN1, sheet, start_date, end_date, timestamp)
    process_account(CAMPAIGN_IDS2, JWT_TOKEN2, sheet, start_date, end_date, timestamp)

if __name__ == "__main__":
    main()
