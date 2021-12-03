from datetime import datetime
import os
import pytz
import requests
import math
import pandas as pd

API_KEY = 'PGXIDH3YRYJ1RSVH'
API_URL_old = 'http://api.openweathermap.org/data/2.5/weather?q={}&mode=json&units=metric&appid={}'
API_URL = 'https://www.alphavantage.co/query?function={}&symbol={}&apikey={}'
time_series_monthly = "TIME_SERIES_MONTHLY"
# function = "TIME_SERIES_MONTHLY"


def query_api(name):
    try:
        print(API_URL.format(time_series_monthly, name, API_KEY))
        data = requests.get(API_URL.format(time_series_monthly, name, API_KEY)).json()
        return data
    except Exception as exc:
        print(exc)
        data = None
        return data

