import os
import re
import json
import datetime
import gspread
from google.oauth2.service_account import Credentials
import base64


# Function to extract ticker from tweet text
def extract_ticker(tweet_text):
    match = re.search(r"\(\$([A-Z]+)\)", tweet_text)
    return match.group(1) if match else None

# Load and parse tweets data
def load_tweets_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        json_str = content.split('=', 1)[1].strip()
        tweets_data = json.loads(json_str)
    return tweets_data

creds_json = base64.b64decode(os.environ['GSPREAD_CREDENTIALS']).decode('utf-8')
creds_dict = json.loads(creds_json)

credentials = Credentials.from_service_account_info(creds_dict, scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
gc = gspread.authorize(credentials)
spreadsheet_id = '1Dj2MGJAlWaVPxxuix3vlMMCBq6hVaEpvgL-x_ETDh44'
sheet = gc.open_by_key(spreadsheet_id).get_worksheet(0)

headers = ["Ticker", "Tweet Date and Time"]
sheet.clear()
sheet.append_row(headers)

# Load tweets data
file_path = os.getenv("PATH_TO_TWEETS", "default_path_if_not_set")
tweets_data = load_tweets_data(file_path)

# Sort tweets by date from oldest to newest
sorted_tweets_data = sorted(tweets_data, key=lambda x: datetime.datetime.strptime(x["tweet"]["created_at"], "%a %b %d %H:%M:%S +0000 %Y"))

all_rows = []  # Accumulate all rows to append in a batch

# Process each sorted tweet
for tweet_data in sorted_tweets_data:
    tweet = tweet_data["tweet"]
    ticker = extract_ticker(tweet["full_text"])
    if not ticker:
        continue
    tweet_datetime = datetime.datetime.strptime(tweet["created_at"], "%a %b %d %H:%M:%S +0000 %Y")
    trade_datetime_str = tweet_datetime.strftime("%Y-%m-%d %H:%M:%S")  # Adjusted to simple Date and Time format

    # Prepare row data including the tweet's date and time
    row_data = [ticker, trade_datetime_str]
    all_rows.append(row_data)

# Append all rows in a single batch operation to ensure efficiency
if all_rows:
    sheet.append_rows(all_rows)

print(f"Successfully appended {len(all_rows)} rows.")
