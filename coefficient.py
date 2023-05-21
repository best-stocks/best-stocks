import alphavintage

def pe_ratio(ticker):
    return alphavintage.get_info_by_ticker(ticker=ticker)["pe_ratio"]

def pb_ratio(ticker):
    return alphavintage.get_info_by_ticker(ticker=ticker)["pb_ratio"]

def ps_ratio(ticker):
    return alphavintage.get_info_by_ticker(ticker=ticker)["ps_ratio"]

def get_graham_number(ticker):
    debt = ticker["debt"]
    shares_outstanding = ticker["shares_outstanding"]
    assets = ticker["assets"]
    return (assets - debt) / shares_outstanding

def get_graham_percent(ticker):
    graham_number = get_graham_number(ticker=ticker)
    current_price = ticker["current_price"]
    return current_price / graham_number