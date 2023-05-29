import requests
from dotenv import dotenv_values, load_dotenv

load_dotenv()

API_KEY = dotenv_values().get("API_KEY")

def get_info_by_ticker(ticker):
    url = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={ticker}&apikey={API_KEY}'

    response = requests.get(url)
    
    data = response.json()
    fiscalDateEndings = []
    revenue = data['annualReports'][0]['totalRevenue']
    
    revenues = []
    for annualReport in data['annualReports']:
        revenues.append(annualReport['totalRevenue'])
        fiscalDateEndings.append(annualReport['fiscalDateEnding'])
    
    url = f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={ticker}&apikey={API_KEY}'

    response = requests.get(url)
    
    data = response.json()
    debt = data['annualReports'][0]['totalLiabilities']
    
    debts = []
    for annualReport in data['annualReports']:
        debts.append(annualReport['totalLiabilities'])
    
    assets = data['annualReports'][0]['totalAssets']
    
    current_assets = data['annualReports'][0]['totalCurrentAssets']
    
    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={API_KEY}'

    response = requests.get(url)
    
    data = response.json()
    
    pe_ratio = data['PERatio']
    pb_ratio = data['PriceToBookRatio']
    ps_ratio = data['PriceToSalesRatioTTM']
    
    evt_ebitda_ratio = data['EVToEBITDA']
    market_cap = data['MarketCapitalization']
    shares_outstanding = data['SharesOutstanding']
    
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={API_KEY}'
    
    response = requests.get(url)
    
    data = response.json()
    
    current_price = data['Global Quote']['05. price']
    
    url = f'https://www.alphavantage.co/query?function=CASH_FLOW&symbol={ticker}&apikey={API_KEY}'

    response = requests.get(url)
    
    data = response.json()
    cashflow = data['annualReports'][0]['operatingCashflow']

    return {
        'ticker': ticker, # +
        'current_price': float(current_price), # + Цена акции
        'assets': int(assets), # + Активы
        'current_assets': int(current_assets), # + Чистые активы
        'pe_ratio': float(pe_ratio), # +
        'pb_ratio': float(pb_ratio), # + P/BV
        'ps_ratio': float(ps_ratio), # +
        'evt_ebitda_ratio': float(evt_ebitda_ratio), # +
        'debt': int(debt), # + Долг
        'revenue': int(revenue), # + Выручка
        'market_cap': int(market_cap), # + Капитализация
        'shares_outstanding': int(shares_outstanding), # + Число акций
        'cashflow': int(cashflow), # + Операционный денежный поток
    }, {
        'ticker': ticker,
        'fiscalDateEndings': fiscalDateEndings,
        'revenues': revenues,
        'debts': debts,
    }
