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
    
    balance_infos = []
    stocks = []
    for ticker in tqdm(tickers):
        stock, balance_info = alphavintage.get_info_by_ticker(ticker=ticker)
        stocks.append(stock)
        balance_infos.append(balance_info)
        time.sleep(TIME_SLEEP)
    
    with open('stocks.json', 'w') as file:
        json.dump(stocks, file)
        
    with open('balance.json', 'w') as file:
        json.dump(balance_infos, file)

update_required = input("Нужно ли обновить датасет? (да/нет): ").lower() == 'да'

if update_required:
    update_dataset()
    print("Датасет успешно обновлен.\n")

with open('stocks.json', 'r') as file:
    stocks = json.load(file)
    
with open('balance.json', 'r') as file:
    balance_infos = json.load(file)

stock_weights_dict = {}
coef_stock_dict = {}

def min_stock(old_stock, ticker, coef):
    min_stock = min(old_stock[1], coef)
    if min_stock == old_stock[1]:
        return old_stock
    else:
        return (ticker, coef)

for stock in stocks:
    weight = 0

    ticker = stock['ticker']
    pe_ratio = stock['pe_ratio']
    ps_ratio = stock['ps_ratio']
    pb_ratio = stock['pb_ratio']
    evt_ebitda_ratio = stock['evt_ebitda_ratio']
    debt = stock['debt']
    assets = stock['assets']
    
    p_cf_ratio = coefficient.get_p_cf_ratio(stock=stock)
    graham = coefficient.get_graham_percent(stock=stock)
    debt_to_cap = coefficient.get_debt_to_cap(stock=stock)
    current_assets_to_cap = coefficient.get_current_assets_to_market_cap(stock=stock)
    
    if assets > debt:
        if pb_ratio < 0.75:
            weight += 1
        elif pb_ratio > 1:
            weight -= 1
            
        if 'pb_ratio' in coef_stock_dict:
            coef_stock_dict['pb_ratio'] = min_stock(coef_stock_dict['pb_ratio'], ticker, pb_ratio)
        else:
            coef_stock_dict['pb_ratio'] = (ticker, pb_ratio)
        
        if debt_to_cap < 0.1:
            weight += 1
        else:
            weight -= 1
           
        if 'debt_to_cap' in coef_stock_dict:
            coef_stock_dict['debt_to_cap'] = min_stock(coef_stock_dict['debt_to_cap'], ticker, debt_to_cap)
        else: 
            coef_stock_dict['debt_to_cap'] = (ticker, debt_to_cap)
            
        if ps_ratio < 1:
            weight += 1
        elif ps_ratio > 2:
            weight -= 1
        
        if 'ps_ratio' in coef_stock_dict:
            coef_stock_dict['ps_ratio'] = min_stock(coef_stock_dict['ps_ratio'], ticker, ps_ratio)
        else:
            coef_stock_dict['ps_ratio'] = (ticker, ps_ratio)

        if graham > 50 and graham < 70:
            weight += 1
        elif graham > 70:
            weight -= 1
            
        if 'graham' in coef_stock_dict:
            coef_stock_dict['graham'] = min_stock(coef_stock_dict['graham'], ticker, graham)
        else:
            coef_stock_dict['graham'] = (ticker, graham)
        
        if pe_ratio < 12:
            weight += 1
        elif pe_ratio > 20:
            weight -= 1
        
        if 'pe_ratio' in coef_stock_dict:
            coef_stock_dict['pe_ratio'] = min_stock(coef_stock_dict['pe_ratio'], ticker, pe_ratio)
        else:
            coef_stock_dict['pe_ratio'] = (ticker, pe_ratio)
            
        if p_cf_ratio < 15:
            weight += 1
        elif p_cf_ratio > 20:
            weight -= 1
        
        if 'p_cf_ratio' in coef_stock_dict:
            coef_stock_dict['p_cf_ratio'] = min_stock(coef_stock_dict['p_cf_ratio'], ticker, p_cf_ratio)
        else:
            coef_stock_dict['p_cf_ratio'] = (ticker, p_cf_ratio)
        
        if evt_ebitda_ratio < 10:
            weight += 1
        
        if 'evt_ebitda_ratio' in coef_stock_dict:
            coef_stock_dict['evt_ebitda_ratio'] = min_stock(coef_stock_dict['evt_ebitda_ratio'], ticker, evt_ebitda_ratio)
        else:
            coef_stock_dict['evt_ebitda_ratio'] = (ticker, evt_ebitda_ratio)
        
        if current_assets_to_cap > 0.95:
            weight += 1
        
        if 'current_assets_to_cap' in coef_stock_dict:
            coef_stock_dict['current_assets_to_cap'] = min_stock(coef_stock_dict['current_assets_to_cap'], ticker, current_assets_to_cap)
        else:   
            coef_stock_dict['current_assets_to_cap'] = (ticker, current_assets_to_cap)
        
        stock_weights_dict[ticker] = (weight, 0)

for coef, info in coef_stock_dict.items():
    ticker = info[0]
    cur_win = stock_weights_dict[ticker][1]
    stock_weights_dict[ticker] = (stock_weights_dict[ticker][0], cur_win + 1)

stock_weights = []
for ticker, info in stock_weights_dict.items():
    stock_weights.append((ticker, info[0], info[1]))

print(stock_weights)

stock_weights = sorted(stock_weights, key = lambda stock: (stock[1], stock[2]))

print('Winner: ', stock_weights[-1][0])

graphic.print_charts(stocks=stocks)
graphic.print_balance_graphic(balance_infos=balance_infos)
graphic.print_ratios_graphic(stocks=stocks)
