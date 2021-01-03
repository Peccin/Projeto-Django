import re
import json
import csv
from bs4 import BeautifulSoup
from io import StringIO
import requests

stock_url = 'https://query1.finance.yahoo.com/v7/finance/download/{}?'
stock = 'F'

params = {
    # 'period1': '1577828735',
    # 'period2': '1609451135',
    'range': '5y',
    'interval': '1d',
    'events': 'history'
}

response = requests.get(stock_url.format(stock), params=params)

file = StringIO(response.text)
reader = csv.reader(file)
data = list(reader)
for row in data[:100]:
    print(row)
