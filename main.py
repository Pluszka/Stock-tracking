import os
import requests
import math
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHA_LINK = 'https://www.alphavantage.co/query'
NEWS_LINK = 'https://newsapi.org/v2/everything'

def compare_prices(yesterday, before_yesterday):
    five_percent = before_yesterday * 0.01
    difference = before_yesterday - yesterday
    if math.fabs(difference) >= five_percent:
        return True
    return False

parameters_stock = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK,
    'datatype': 'json',
    'apikey': os.environ.get('ALPHA_API_KEY')
}

response = requests.get(url=ALPHA_LINK, params=parameters_stock)
response.raise_for_status()
data = response.json()['Time Series (Daily)']
list_of_days = [value for (key, value) in data.items()]
yesterday_closing = float(list_of_days[0]['4. close'])
day_before_yesterday_closing = float(list_of_days[1]['4. close'])
print(yesterday_closing, day_before_yesterday_closing)


if compare_prices(yesterday_closing, day_before_yesterday_closing) or True:
    parameters_news = {
        'qInTitle': COMPANY_NAME,
        'apiKey': os.environ.get('NEWS_API_KEY')
    }
    response = requests.get(url=NEWS_LINK, params=parameters_news)
    response.raise_for_status()
    data = response.json()['articles'][:3]
    articles_list = [f"Headline: {article['title']}.\n Brief: {article['description']}\n{article['url']}\n" for article in data]
    client = Client(os.environ.get('account_sid'), os.environ.get('auth_token'))
    message = client.messages \
        .create(
        body=articles_list,
        from_='+18126339019',
        to=os.environ.get('my_phone')
    )
    print(message.status)

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

