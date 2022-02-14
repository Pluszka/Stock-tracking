import os
import requests
import math

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHA_LINK = 'https://www.alphavantage.co/query'

def compare_prices(yesterday, before_yesterday):
    five_percent = before_yesterday * 0.05
    difference = before_yesterday - yesterday
    if math.fabs(difference) >= five_percent:
        return True
    return False

parameters = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK,
    'datatype': 'json',
    'apikey': os.environ.get('ALPHA_API_KEY')
}

response = requests.get(url=ALPHA_LINK, params=parameters)
response.raise_for_status()
data = response.json()['Time Series (Daily)']
list_of_days = [value for (key, value) in data.items()]
yesterday_closing = float(list_of_days[0]['4. close'])
day_before_yesterday_closing = float(list_of_days[1]['4. close'])
print(yesterday_closing, day_before_yesterday_closing)


if compare_prices(yesterday_closing, day_before_yesterday_closing):
    print('NEws')


## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.


#Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

