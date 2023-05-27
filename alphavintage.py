import requests
from dotenv import dotenv_values, load_dotenv

load_dotenv()

API_KEY = dotenv_values().get("API_KEY")

def get_info_by_ticker(ticker):
    url = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={ticker}&apikey={API_KEY}'

    response = requests.get(url)
    if response.status_code != 200:
        return {}, {}, ConnectionError
    
    data = response.json()
    fiscalDateEndings = []
    revenue = data['annualReports'][0]['totalRevenue']
    if revenue == '-' or revenue == 'None':
        return {}, {}, ValueError
    
    revenues = []
    for annualReport in data['annualReports']:
        revenues.append(annualReport['totalRevenue'])
        fiscalDateEndings.append(annualReport['fiscalDateEnding'])
    
    url = f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={ticker}&apikey={API_KEY}'

    response = requests.get(url)
    if response.status_code != 200:
        return {}, {}, ConnectionError
    
    data = response.json()
    debt = data['annualReports'][0]['totalLiabilities']
    if debt == '-' or debt == 'None':
        return {}, {}, ValueError
    
    debts = []
    for annualReport in data['annualReports']:
        debts.append(annualReport['totalLiabilities'])
    
    assets = data['annualReports'][0]['totalAssets']
    if assets == '-' or assets == 'None':
        return {}, {}, ValueError
    
    current_assets = data['annualReports'][0]['totalCurrentAssets']
    if current_assets == '-' or current_assets == 'None':
        return {}, {}, ValueError
    
    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={API_KEY}'

    response = requests.get(url)
    if response.status_code != 200:
        return {}, {}, ConnectionError
    
    data = response.json()
    
    pe_ratio = data['PERatio']
    if pe_ratio == '-' or pe_ratio == 'None':
        return {}, {}, ValueError
    
    pb_ratio = data['PriceToBookRatio']
    if pb_ratio == '-' or pb_ratio == 'None':
        return {}, {}, ValueError
    
    ps_ratio = data['PriceToSalesRatioTTM']
    if ps_ratio == '-' or ps_ratio == 'None':
        return {}, {}, ValueError
    
    evt_ebitda_ratio = data['EVToEBITDA']
    if evt_ebitda_ratio == '-' or evt_ebitda_ratio == 'None':
        return {}, {}, ValueError
    
    market_cap = data['MarketCapitalization']
    if market_cap == '-' or market_cap == 'None':
        return {}, {}, ValueError
    
    shares_outstanding = data['SharesOutstanding']
    if shares_outstanding == '-' or shares_outstanding == 'None':
        return {}, {}, ValueError
    
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={API_KEY}'
    response = requests.get(url)
    if response.status_code != 200:
        return {}, {}, ConnectionError
    
    data = response.json()
    
    current_price = data['Global Quote']['05. price']
    if current_price == '-' or current_price == 'None':
        return {}, {}, ValueError
    
    url = f'https://www.alphavantage.co/query?function=CASH_FLOW&symbol={ticker}&apikey={API_KEY}'

    response = requests.get(url)
    if response.status_code != 200:
        return {}, {}, ConnectionError
    
    data = response.json()
    cashflow = data['annualReports'][0]['operatingCashflow']
    if cashflow == '-' or cashflow == 'None':
        return {}, {}, ValueError
    
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
    }, None
