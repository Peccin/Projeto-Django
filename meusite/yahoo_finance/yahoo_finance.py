import re
import json
import csv
from bs4 import BeautifulSoup
from io import StringIO
import requests

url_stats = 'https://finance.yahoo.com/quote/{}/key-statistics?p={}'
url_profile = 'https://finance.yahoo.com/quote/{}/profile?p={}'
url_financials = 'https://finance.yahoo.com/quote/{}/financials?p={}'

stock = 'F'

response = requests.get(url_financials.format(stock, stock))

soup = BeautifulSoup(response.text, 'html.parser')

pattern = re.compile(r'\s--\sData\s--\s')
script_data = soup.find('script', text=pattern).contents[0]

start = script_data.find("context")-2
json_data = json.loads(script_data[start:-12])

json_data['context'].keys()

json_data['context']['dispatcher']['stores']['QuoteSummaryStore'].keys()

annual_is = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['incomeStatementHistory']['incomeStatementHistory']
quarterly_is = json_data['context']['dispatcher']['stores']['QuoteSummaryStore'][
    'incomeStatementHistoryQuarterly']['incomeStatementHistory']

annual_cf = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['cashflowStatementHistory']['cashflowStatements']
quarterly_cf = json_data['context']['dispatcher']['stores'][
    'QuoteSummaryStore']['cashflowStatementHistoryQuarterly']['cashflowStatements']

annual_bs = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['balanceSheetHistory']['balanceSheetStatements']
quarterly_bs = json_data['context']['dispatcher']['stores'][
    'QuoteSummaryStore']['balanceSheetHistoryQuarterly']['balanceSheetStatements']

annual_is_stmts = []
# consolidate annual
for s in annual_is:
    statement = {}
    for key, val in s.items():
        try:
            statement[key] = val['raw']
        except TypeError:
            continue
        except KeyError:
            continue
annual_is_stmts.append(statement)

annual_cf_stmts = []
# annual
for s in annual_cf:
    statement = {}
    for key, val in s.items():
        try:
            statement[key] = val['raw']
        except TypeError:
            continue
        except KeyError:
            continue
annual_cf_stmts.append(statement)

quarterly_cf_stmts = []
# quarterly
for s in quarterly_cf:
    statement = {}
    for key, val in s.items():
        try:
            statement[key] = val['raw']
        except TypeError:
            continue
        except KeyError:
            continue
quarterly_cf_stmts.append(statement)


# Profile Data

response = requests.get(url_profile.format(stock, stock))
soup = BeautifulSoup(response.text, 'html.parser')
pattern = re.compile(r'\s--\sData\s--\s')
script_data = soup.find('script', text=pattern).contents[0]
start = script_data.find("context")-2
json_data = json.loads(script_data[start:-12])

json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['assetProfile'].keys()

# Statistics

response = requests.get(url_stats.format(stock, stock))
soup = BeautifulSoup(response.text, 'html.parser')
pattern = re.compile(r'\s--\sData\s--\s')
script_data = soup.find('script', text=pattern).contents[0]
start = script_data.find("context")-2
json_data = json.loads(script_data[start:-12])

json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['assetProfile'].keys()

print(json_data)
