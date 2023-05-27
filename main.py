import alphavintage
import coefficient
import time
import json
from tqdm import tqdm
import graphic
import smart_lab
import matplotlib.pyplot as plt

TIME_SLEEP = 60

EN_TICKERS_PATH = 'tickers/en'
RU_TICKERS_PATH = 'tickers/ru'

EN_DATASET_PATH = 'dataset/en'
RU_DATASET_PATH = 'dataset/ru'

def update_dataset():
    tickers = []

    with open(f'{EN_TICKERS_PATH}/top3.txt', 'r') as file:
        for line in file:
            ticker = line.strip()
            tickers.append(ticker)
    
    balance_infos = []
    stocks = []
    error_tickers = []
    
    for ticker in tqdm(tickers):
        stock, balance_info, err = alphavintage.get_info_by_ticker(ticker=ticker)
        if err != None:
            time.sleep(TIME_SLEEP)
            error_tickers.append(ticker)
            continue
        
        print(ticker)
        stocks.append(stock)
        balance_infos.append(balance_info)
        time.sleep(TIME_SLEEP)
    
    with open(f'{EN_DATASET_PATH}/3stocks.json', 'w') as file:
        json.dump(stocks, file)
        
    with open(f'{EN_DATASET_PATH}/3balances.json', 'w') as file:
        json.dump(balance_infos, file)
    
    with open('error_tickers.txt', 'w') as file:
        ticker_string = '\n'.join(error_tickers)
        file.write(ticker_string)

exchange = input("Выберите рынок акций? (RU/EN): ").lower()
if(exchange == "ru"):
    tickers = []
    update_required = input("Нужно ли обновить датасет? (Y/N): ").lower() == 'да'
    if update_required:
        with open(f'{RU_TICKERS_PATH}/ru_tickers.txt', 'r') as file:
            for line in file:
                ticker = line.strip()
                tickers.append(ticker)
        del_tickers = smart_lab.make_data(tickers,"2021", "all_ru_data_2021.csv")
        tickers = list(set(tickers) - set(del_tickers))
        with open(f'{RU_TICKERS_PATH}/ru_last_all_work_tickers.txt', 'w') as file:
            ticker_string = '\n'.join(tickers)
            file.write(ticker_string)
    else:
        with open(f'{RU_TICKERS_PATH}/ru_last_all_work_tickers.txt', 'r') as file:
            for line in file:
                ticker = line.strip()
                tickers.append(ticker)

    stocks = []
    for ticker in tickers:
        stock = smart_lab.get_values_by_tiker(f'{RU_DATASET_PATH}/all_ru_data_2021.csv', ticker)
        if(stock['cashflow'] != 0.0):
            stocks.append(stock)
        print(ticker)

else:
    update_required = input("Нужно ли обновить датасет? (Y/N): ").lower() == 'да'

    if update_required:
        update_dataset()
        print("Датасет успешно обновлен.\n")

    with open(f'{EN_DATASET_PATH}/3stocks.json', 'r') as file:
        stocks = json.load(file)

    with open(f'{EN_DATASET_PATH}/3balances.json', 'r') as file:
        balance_infos = json.load(file)

stock_weights_dict = {}
coef_stock_dict = {}

stocks_dict = {}
for stock in stocks:
    stocks_dict[stock['ticker']] = stock

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

if len(stock_weights) >= 10:
    top10_tickers = stock_weights[:5] + stock_weights[-5:]
else:
    top10_tickers = stock_weights

if len(stock_weights) >= 30:
    top30_tickers = stock_weights[:15] + stock_weights[-15:]
else:
    top30_tickers = stock_weights
    
top10 = []
for item in top10_tickers:
    stock = stocks_dict[item[0]]
    top10.append(stock)
    
top30 = []
for item in top30_tickers:
    stock = stocks_dict[item[0]]
    top30.append(stock)

def print_scores_of_stock(stock):
    print('Scores: ', stock[1])
    print('Count of wins: ', stock[2])
    print()

print('🏆 Top 3: 🏆')
print('🥇 ', stock_weights[-1][0])
print_scores_of_stock(stock_weights[-1])

print('🥈 ', stock_weights[-2][0])
print_scores_of_stock(stock_weights[-2])

print('🥉 ', stock_weights[-3][0])
print_scores_of_stock(stock_weights[-3])

# All stocks
graphic.print_bubble_charts(stocks=top30)

# Large sample
graphic.print_bar_chart(stocks=top30)

# Small sample
graphic.print_pie_charts(stocks=top10)

# graphic.print_balance_graphic(balance_infos=balance_infos)
# graphic.print_ratios_graphic(stocks=stocks)
plt.show()
