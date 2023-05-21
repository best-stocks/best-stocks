import alphavintage
import coefficient
import time
import json
from tqdm import tqdm

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
    print("Датасет успешно обновлен.")

with open('dataset.json', 'r') as file:
    stocks = json.load(file)

for stock in stocks:
    pe_ratio = stock['pe_ratio']
    ps_ratio = stock['ps_ratio']
    pb_ratio = stock['pb_ratio']
    peg_ratio = stock['peg_ratio']
    evt_ebitda_ratio = stock['evt_ebitda_ratio']
    
    p_cf_ratio = coefficient.get_p_cf_ratio(stock=stock)
    graham = coefficient.get_graham_percent(stock=stock)
    debt_to_cap = coefficient.get_debt_to_cap(stock=stock)
    current_assets_to_cap = coefficient.get_current_assets_to_market_cap(stock=stock)
    