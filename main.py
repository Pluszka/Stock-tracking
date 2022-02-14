import os
import requests
import math
from twilio.rest import Client

percent: int
event_emoji: str
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHA_LINK = 'https://www.alphavantage.co/query'
NEWS_LINK = 'https://newsapi.org/v2/everything'

UP_EMOJI = '🔺'
DOWN_EMOJI = '🔻'

def compare_prices(yesterday, before_yesterday):
    global event_emoji
    global percent
    five_percent = before_yesterday * 0.05
    difference = before_yesterday - yesterday
    percent = yesterday / before_yesterday - 1
    if percent > 0:
        event_emoji = UP_EMOJI
    else:
        event_emoji = DOWN_EMOJI
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

if compare_prices(yesterday_closing, day_before_yesterday_closing) or True:
    parameters_news = {
        'qInTitle': COMPANY_NAME,
        'apiKey': os.environ.get('NEWS_API_KEY')
    }

    response = requests.get(url=NEWS_LINK, params=parameters_news)
    response.raise_for_status()
    data = response.json()['articles'][:3]

    articles_list = [f"{STOCK}: {event_emoji}{round(percent, 5)}%\nHeadline: {article['title']}.\n Brief: {article['description']}\n{article['url']}\n" for article in data]
    client = Client(os.environ.get('account_sid'), os.environ.get('auth_token'))

    for article in articles_list:
        message = client.messages \
            .create(
            body=article,
            from_='+18126339019',
            to=os.environ.get('my_phone')
        )
    print(message.status)
