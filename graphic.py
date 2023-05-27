import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

tickers = []
pe_ratios = []
pb_ratios = []
ps_ratios = []
evt_ebitda_ratios = []
market_caps = []
ratios = []
revenues = []
assets = []
debts = []

def reset_data():
    global tickers, pe_ratios, pb_ratios, ps_ratios, market_caps, volumes, ratios, revenues, assets, debts, evt_ebitda_ratios
    tickers = []
    pe_ratios = []
    pb_ratios = []
    ps_ratios = []
    market_caps = []
    ratios = []
    revenues = []
    assets = []
    debts = []
    evt_ebitda_ratios = []

def set_data(stocks):
    for stock in stocks:
        tickers.append(stock['ticker'])
        pe_ratios.append(stock['pe_ratio'])
        pb_ratios.append(stock['pb_ratio'])
        ps_ratios.append(stock['ps_ratio'])
        market_caps.append(stock['market_cap'])
        ratios.append([stock['pe_ratio'], stock['pb_ratio'], stock['ps_ratio'], stock['evt_ebitda_ratio']])  
        revenues.append(stock['revenue'])
        assets.append(stock['assets'])
        debts.append(stock['debt'])
        evt_ebitda_ratios.append(stock['evt_ebitda_ratio'])

def print_bar_chart(stocks):
    set_data(stocks=stocks)

    plt.figure(1)
    plt.subplot(1, 1, 1)
    plt.bar(tickers, market_caps)
    plt.title('Market Capitalization')
    plt.xlabel('Companies')
    plt.ylabel('Market Cap (in billions)')
    
    # ----------------------------------------------------------
    
    # plt.figure(2)
    # plt.subplot(1, 3, 1)
    # plt.scatter(market_caps, pe_ratios, s=100, alpha=0.5)
    # for i in range(len(tickers)):
    #     plt.text(market_caps[i], pe_ratios[i], tickers[i])
    # plt.title('Market Cap vs. P/E Ratio')
    # plt.xlabel('Market Cap (in billions)')
    # plt.ylabel('P/E Ratio')
    
    # plt.subplot(1, 3, 2)
    # plt.scatter(market_caps, ps_ratios, s=100, alpha=0.5)
    # for i in range(len(tickers)):
    #     plt.text(market_caps[i], ps_ratios[i], tickers[i])
    # plt.title('Market Cap vs. P/S Ratio')
    # plt.xlabel('Market Cap (in billions)')
    # plt.ylabel('P/S Ratio')
    
    # plt.subplot(1, 3, 3)
    # plt.scatter(market_caps, pb_ratios, s=100, alpha=0.5)
    # for i in range(len(tickers)):
    #     plt.text(market_caps[i], pb_ratios[i], tickers[i])
    # plt.title('Market Cap vs. P/B Ratio')
    # plt.xlabel('Market Cap (in billions)')
    # plt.ylabel('P/B Ratio')
    
def print_bubble_charts(stocks):
    reset_data()
    set_data(stocks=stocks)
    
    bubble_sizes = [mc / 1e9 for mc in market_caps]
    
    plt.figure(3)
    plt.scatter(revenues, debts, s=bubble_sizes, alpha=0.5)

    plt.xlabel('Revenue (USD)')
    plt.ylabel('Debt (USD)')
    plt.title('Bubble Chart: Revenue vs Debt')

    # Add annotations for ticker symbols
    for i in range(len(stocks)):
        plt.annotate(tickers[i], (revenues[i], debts[i]), ha='center', va='center')
        
    # ----------------------------------------------------------
    
    plt.figure(4)
    plt.scatter(pe_ratios, ps_ratios, s=bubble_sizes, alpha=0.5)

    plt.xlabel('P/E Ratio')
    plt.ylabel('P/S Ratio')
    plt.title('Bubble Chart: P/E Ratio vs P/S Ratio')

    # Add annotations for ticker symbols
    for i in range(len(stocks)):
        plt.annotate(tickers[i], (pe_ratios[i], ps_ratios[i]), ha='center', va='center')
    
    # ----------------------------------------------------------
    
    plt.figure(5)
    plt.scatter(pb_ratios, evt_ebitda_ratios, s=bubble_sizes, alpha=0.5)

    plt.xlabel('P/B Ratio')
    plt.ylabel('EVT/EBITDA Ratio')
    plt.title('Bubble Chart: P/B Ratio vs EVT/EBITDA Ratio')

    # Add annotations for ticker symbols
    for i in range(len(stocks)):
        plt.annotate(tickers[i], (pb_ratios[i], evt_ebitda_ratios[i]), ha='center', va='center')

def print_pie_charts(stocks):
    reset_data()
    set_data(stocks=stocks)
    
    plt.figure(2)
    plt.subplot(1, 3, 1)
    plt.pie(assets, labels=tickers, autopct='%1.1f%%')
    plt.title('Assets')
    
    plt.subplot(1, 3, 2)
    plt.pie(revenues, labels=tickers, autopct='%1.1f%%')
    plt.title('Revenues')
    
    plt.subplot(1, 3, 3)
    plt.pie(debts, labels=tickers, autopct='%1.1f%%')
    plt.title('Debts')
    
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

def print_heatmap_graphic(stocks):    
    filtered_data = [company for company in stocks if company['revenue'] > 30e9 and company['revenue'] < 1000e9]
    
    debt = np.array([company['debt'] for company in filtered_data]) / 1e9  # Разделение debt на сотни миллионов
    revenue = np.array([company['revenue'] for company in filtered_data]) / 1e9  # Разделение revenue на сотни миллионов

    heatmap, xedges, yedges = np.histogram2d(debt, revenue, bins=14)  # Создание тепловой карты

    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    plt.figure(figsize=(8, 6))
    plt.imshow(heatmap.T, origin='lower', cmap='coolwarm', extent=extent, aspect='auto')

    plt.colorbar(label='Number of Companies')
    plt.xlabel('Debt (in milliards)')
    plt.ylabel('Revenue (in milliards)')
    
    x_ticks = np.arange(min(debt), max(debt) + 1, 100)  # Шаг 1 миллиард
    y_ticks = np.arange(min(revenue), max(revenue) + 1, 100)  # Шаг 1 миллиард
    plt.xticks(x_ticks)
    plt.yticks(y_ticks)

    plt.title('Heatmap of Debt and Revenue')
    
    # ----------------------------------------------------------
    
    filtered_data = [company for company in stocks if  company['revenue'] < 300e9]
    
    debt = np.array([company['debt'] for company in filtered_data]) / 1e9  # Разделение debt на сотни миллионов
    revenue = np.array([company['revenue'] for company in filtered_data]) / 1e9  # Разделение revenue на сотни миллионов

    heatmap, xedges, yedges = np.histogram2d(debt, revenue, bins=14)  # Создание тепловой карты

    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    plt.figure(figsize=(8, 6))
    plt.imshow(heatmap.T, origin='lower', cmap='coolwarm', extent=extent, aspect='auto')

    plt.colorbar(label='Number of Companies')
    plt.xlabel('Debt (in milliards)')
    plt.ylabel('Revenue (in milliards)')
    
    x_ticks = np.arange(min(debt), max(debt) + 1, 20)
    y_ticks = np.arange(min(revenue), max(revenue) + 1, 20)
    plt.xticks(x_ticks)
    plt.yticks(y_ticks)

    plt.title('Heatmap of Debt and Revenue Small')
