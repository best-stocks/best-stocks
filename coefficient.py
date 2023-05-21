import alphavintage

def get_graham_number(stock):
    debt = stock["debt"]
    shares_outstanding = stock["shares_outstanding"]
    assets = stock["assets"]
    return (assets - debt) / shares_outstanding

def get_graham_percent(stock):
    graham_number = get_graham_number(stock=stock)
    current_price = stock["current_price"]
    return current_price / graham_number * 100
