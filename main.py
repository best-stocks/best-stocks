import alphavintage
import coefficient
import time
import json
from tqdm import tqdm
import graphic

TIME_SLEEP = 60

def update_dataset():
    tickers = []

    with open('top3.txt', 'r') as file:
        for line in file:
            ticker = line.strip() 
            tickers.append(ticker)
    
    stocks = []
    for ticker in tqdm(tickers):
        info = alphavintage.get_info_by_ticker(ticker=ticker)
        stocks.append(info)
        time.sleep(TIME_SLEEP)
    
    with open('dataset.json', 'w') as file:
        json.dump(stocks, file)

update_required = input("Нужно ли обновить датасет? (да/нет): ").lower() == 'да'

if update_required:
    update_dataset()
    print("Датасет успешно обновлен.\n")
    
amount = int(input("Введите сумму, которую готовы потратить на покупку акций (в долларах): "))

with open('dataset.json', 'r') as file:
    stocks = json.load(file)

stock_weights = []

for stock in stocks:
    weight = 0
    
    ticker = stock['ticker']
    pe_ratio = stock['pe_ratio']
    ps_ratio = stock['ps_ratio']
    pb_ratio = stock['pb_ratio']
    peg_ratio = stock['peg_ratio']
    evt_ebitda_ratio = stock['evt_ebitda_ratio']
    volume = stock['volume']
    debt = stock['debt']
    assets = stock['assets']
    
    p_cf_ratio = coefficient.get_p_cf_ratio(stock=stock)
    graham = coefficient.get_graham_percent(stock=stock)
    debt_to_cap = coefficient.get_debt_to_cap(stock=stock)
    current_assets_to_cap = coefficient.get_current_assets_to_market_cap(stock=stock)
    
    if assets > debt and volume > amount * 100:
        if pb_ratio < 0.75:
            weight += 1
        elif pb_ratio > 1:
            weight -= 1
        
        if debt_to_cap < 0.1:
            weight += 1
        else:
            weight -= 1
            
        if ps_ratio < 1:
            weight += 1
        elif ps_ratio > 2:
            weight -= 1

        if graham > 50 and graham < 70:
            weight += 1
        elif graham > 70:
            weight -= 1
        
        if pe_ratio < 12:
            weight += 1
        elif pe_ratio > 20:
            weight -= 1
            
        if p_cf_ratio < 15:
            weight += 1
        elif p_cf_ratio > 20:
            weight -= 1
            
        if peg_ratio < 1:
            weight += 1
            
        if evt_ebitda_ratio < 10:
            weight += 1
        
        if current_assets_to_cap > 0.95:
            weight += 1
        
        stock_weights.append((ticker, weight))

print(stock_weights)
winner = max(stock_weights)
print(winner)

graphic.print_charts(stocks=stocks)
