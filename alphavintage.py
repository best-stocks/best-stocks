import requests
from dotenv import dotenv_values, load_dotenv

# Load environment variables from .env file
load_dotenv()

# Замените YOUR_API_KEY на ваш ключ API Alpha Vantage
API_KEY = dotenv_values().get("API_KEY")

def get_info_by_ticker(ticker):
    # Запрос к API Alpha Vantage для получения выручки компании
    url = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={ticker}&apikey={API_KEY}'

    response = requests.get(url)
    data = response.json()
    revenue = data['annualReports'][0]['totalRevenue']
    
    url = f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={ticker}&apikey={API_KEY}'

    response = requests.get(url)
    data = response.json()
    debt = data['annualReports'][0]['totalLiabilities']
    
    assets = data['annualReports'][0]['totalAssets']
    current_assets = data['annualReports'][0]['totalCurrentAssets']
    
    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={API_KEY}'

    response = requests.get(url)
    data = response.json()
    
    pe_ratio = data['PERatio']
    pb_ratio = data['PriceToBookRatio']
    ps_ratio = data['PriceToSalesRatioTTM']
    peg_ratio = data['PEGRatio']
    evt_ebitda_ratio = data['EVToEBITDA']
    
    market_cap = data['MarketCapitalization']
    shares_outstanding = data['SharesOutstanding']
    
    dividend_per_share = data['DividendPerShare']
    dividend_yield = data['DividendYield']
    
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    
    current_price = data['Global Quote']['05. price']
    volume = data['Global Quote']['06. volume']
    
    url = f'https://www.alphavantage.co/query?function=CASH_FLOW&symbol={ticker}&apikey={API_KEY}'

    response = requests.get(url)
    data = response.json()
    cashflow = data['annualReports'][0]['operatingCashflow']
    
    return {
        'ticker': ticker,
        'current_price': float(current_price),
        'volume': int(volume), # REMOVE
        'assets': int(assets),
        'current_assets': int(current_assets),
        'pe_ratio': float(pe_ratio),
        'peg_ratio': float(peg_ratio),
        'pb_ratio': float(pb_ratio),
        'ps_ratio': float(ps_ratio),
        'evt_ebitda_ratio': float(evt_ebitda_ratio),
        'debt': int(debt), 
        'revenue': int(revenue),
        'market_cap': int(market_cap),
        'shares_outstanding': int(shares_outstanding),
        'dividend_per_share': float(dividend_per_share), # REMOVE
        'dividend_yield': float(dividend_yield), # REMOVE
        'cashflow': int(cashflow),
    }

