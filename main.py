import coefficient

tickers = []

file_path = 'top50.txt'

with open(file_path, 'r') as file:
    for line in file:
        ticker = line.strip() 
        tickers.append(ticker)

for ticker in tickers:
    pe_ratio = coefficient.pe_ratio(ticker=ticker)
    pb_ratio = coefficient.pb_ratio(ticker=ticker)
    ps_ratio = coefficient.ps_ratio(ticker=ticker)