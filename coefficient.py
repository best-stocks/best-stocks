import alphavintage

def pe_ratio(ticker):
    return alphavintage.get_info_by_ticker(ticker=ticker)["pe_ratio"]

def pb_ratio(ticker):
    return alphavintage.get_info_by_ticker(ticker=ticker)["pb_ratio"]

def ps_ratio(ticker):
    return alphavintage.get_info_by_ticker(ticker=ticker)["ps_ratio"]
