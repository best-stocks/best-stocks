def get_p_cf_ratio(stock):
    return stock['current_price'] / stock['cashflow']

def get_graham_number(stock):
    return (stock["assets"] - stock["debt"]) / stock["shares_outstanding"]

def get_graham_percent(stock):
    graham_number = get_graham_number(stock=stock)
    current_price = stock["current_price"]
    return current_price / graham_number * 100

def get_debt_to_cap(stock):
    return stock['debt'] / stock['market_cap']

def get_current_assets_to_market_cap(stock):
    return stock['current_assets'] / stock['market_cap']
