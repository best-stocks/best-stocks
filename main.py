import alphavintage
import coefficient
import time
import json

TIME_SLEEP = 60

def update_dataset():
    tickers = []
    file_path = 'top3.txt'

    with open(file_path, 'r') as file:
        for line in file:
            ticker = line.strip() 
            tickers.append(ticker)
    
    tickers_dict = []
    for ticker in tickers:
        info = alphavintage.get_info_by_ticker(ticker=ticker)
        tickers_dict.append(info)
        time.sleep(TIME_SLEEP)
    
    with open('dataset.json', 'w') as file:
        json.dump(tickers_dict, file)

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
    
    