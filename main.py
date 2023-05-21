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
    graham_number = coefficient.get_graham_number(stock)
    graham_percent = coefficient.get_graham_percent(stock)
    print(f"{stock['ticker']}: {graham_percent}, {graham_number}, {stock['assets']}, {stock['debt']}, {stock['shares_outstanding']}, {stock['current_price']}")
    