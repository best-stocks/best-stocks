import matplotlib.pyplot as plt
import numpy as np

tickers = []
pe_ratios = []
pb_ratios = []
ps_ratios = []
market_caps = []
ratios = []

def reset_data():
    global tickers, pe_ratios, pb_ratios, ps_ratios, market_caps, volumes, ratios
    tickers = []
    pe_ratios = []
    pb_ratios = []
    ps_ratios = []
    market_caps = []
    ratios = []

def set_data(stocks):
    for stock in stocks:
        tickers.append(stock['ticker'])
        pe_ratios.append(stock['pe_ratio'])
        pb_ratios.append(stock['pb_ratio'])
        ps_ratios.append(stock['ps_ratio'])
        market_caps.append(stock['market_cap'])
        ratios.append([stock['pe_ratio'], stock['pb_ratio'], stock['ps_ratio'], stock['evt_ebitda_ratio']])  

def print_charts(stocks):
    set_data(stocks=stocks)

    plt.figure(1)
    plt.subplot(1, 1, 1)
    plt.bar(tickers, market_caps)
    plt.title('Market Capitalization')
    plt.xlabel('Companies')
    plt.ylabel('Market Cap (in billions)')
    
    # ----------------------------------------------------------
    
    plt.figure(2)
    plt.subplot(1, 3, 1)
    plt.scatter(market_caps, pe_ratios, s=100, alpha=0.5)
    for i in range(len(tickers)):
        plt.text(market_caps[i], pe_ratios[i], tickers[i])
    plt.title('Market Cap vs. P/E Ratio')
    plt.xlabel('Market Cap (in billions)')
    plt.ylabel('P/E Ratio')
    
    plt.subplot(1, 3, 2)
    plt.scatter(market_caps, ps_ratios, s=100, alpha=0.5)
    for i in range(len(tickers)):
        plt.text(market_caps[i], ps_ratios[i], tickers[i])
    plt.title('Market Cap vs. P/S Ratio')
    plt.xlabel('Market Cap (in billions)')
    plt.ylabel('P/S Ratio')
    
    plt.subplot(1, 3, 3)
    plt.scatter(market_caps, pb_ratios, s=100, alpha=0.5)
    for i in range(len(tickers)):
        plt.text(market_caps[i], pb_ratios[i], tickers[i])
    plt.title('Market Cap vs. P/B Ratio')
    plt.xlabel('Market Cap (in billions)')
    plt.ylabel('P/B Ratio')

def print_ratios_graphic(stocks):
    reset_data()
    set_data(stocks=stocks)

    labels = ['PE Ratio', 'PB Ratio', 'PS Ratio', 'EV/EBITDA Ratio']
    
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    _, ax = plt.subplots(figsize=(6, 6), subplot_kw={'polar': True})

    for i, ticker_ratios in enumerate(ratios):
        ticker_name = tickers[i]
        ticker_ratios += ticker_ratios[:1]
        ax.fill(angles, ticker_ratios, alpha=0.25, label=ticker_name)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    ax.set_rlabel_position(0)
    ax.set_yticklabels([])

    plt.title('Financial Ratios Radar Chart')

    plt.legend()

    plt.show()

def print_balance_graphic(balance_infos):
    plt.figure(figsize=(10, 6))
    for balance_info in balance_infos:
        plt.plot(balance_info['fiscalDateEndings'], balance_info['debts'], label=balance_info['ticker'])
        
    plt.xlabel('Financial Year')
    plt.ylabel('Debt (in billions)')
    plt.title('Debt of Companies over Financial Years')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
