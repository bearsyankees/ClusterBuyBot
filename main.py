import tweepy
from os import environ
import redis
from datetime import datetime
import re
import pandas as panda
import gspread
from google.oauth2.service_account import Credentials
import base64
import json

debug = False  # do certain things when I run locally

r = redis.from_url(environ.get("REDIS_URL"), encoding="utf-8", decode_responses=True)

creds_json = base64.b64decode(environ['GSPREAD_CREDENTIALS']).decode('utf-8')
creds_dict = json.loads(creds_json)

credentials = Credentials.from_service_account_info(creds_dict, scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
gc = gspread.authorize(credentials)
spreadsheet_id = '1Dj2MGJAlWaVPxxuix3vlMMCBq6hVaEpvgL-x_ETDh44'
sheet = gc.open_by_key(spreadsheet_id).get_worksheet(0)

#get from heroku environment
CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_SECRET = environ['ACCESS_SECRET']
BEARER = environ['BEARER']

# initiate tweepy client and pass my credentials thru
client = tweepy.Client(bearer_token=BEARER, consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET,
                       access_token=ACCESS_KEY, access_token_secret=ACCESS_SECRET)

def append_to_sheet(data):
    first_empty_row = len(sheet.get_all_values()) + 1
    sheet.append_row(data, table_range=f"A{first_empty_row}")

# make the SEC filing date readable to python
def time_format(time):
    return datetime.strptime(time, '%Y-%m-%d %H:%M:%S')

# find where to break tweet if it is over 280 characters
def get_space(s):
    m = 260
    while s[m] != " ":
        m += 1
    return m


# yay pandas made this way easier
def main():
    url = 'http://openinsider.com/latest-cluster-buys'
    tables = panda.read_html(url)  # get all tables on page
    pandaData = tables[11]  # the one I want is the 11th
    data1 = pandaData.to_dict()  # read it into a dictionary
    data = {re.sub(r'[^\x00-\x7F]', ' ', k): v for k, v in data1.items()}  # clean up white space
    # reformat dict so each item is about one ticker
    data = [{key.strip(): data[key][i] for key in data.keys()} for i in range(len(data["X"]))]
    new_date = time_format(data[0]["Filing Date"]) # get filing date in datetime element
    if r.get("latest_stock"):  # if there is a latest date do nothing otherwise set it to when I made this bot.
        pass
    else:
        r.mset({"latest_stock": "2022-02-10 16:10:25"})

    print(r.get("latest_stock"))
    old_date = time_format(r.get("latest_stock"))
    print(data[0]["Filing Date"])
    #print(data)

    if new_date > old_date:
        for stock in data:
            if time_format(stock["Filing Date"]) <= old_date:
                break
            else:
                print(stock)
                tweet_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                text = (
                    "{} (${}) was bought by {} insiders on {} for a price per share of {}, filed to the SEC at {}. These insiders"
                    " purchased {} shares (a value of {}), increasing their total (combined) amount of shares owned by {}. #stock #stocks\n"
                    .format(stock["Company Name"], stock["Ticker"].strip(), stock["Ins"], stock["Trade Date"],
                            stock["Price"],
                            stock["Filing Date"], str(stock["Qty"]), str(stock["Value"])[1:], stock["Own"][1:]))
                print(text)
                if len(text) > 280:
                    m = get_space(text)
                    id = client.create_tweet(text="{}...".format(text[:m]))
                    thread = text[m:].strip()
                    client.create_tweet(text=thread, in_reply_to_tweet_id=id[0]["id"])
                else:
                    client.create_tweet(text=text)
                data_to_append = [stock["Ticker"].strip(), tweet_time]
                append_to_sheet(data_to_append)
        r.mset({"latest_stock": data[0]["Filing Date"]})


if __name__ == "__main__":
    main()
