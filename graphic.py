import matplotlib.pyplot as plt
import numpy as np

def print_bar_chart(stocks):
    tickers = [company['ticker'] for company in stocks]
    market_caps = [company['market_cap'] for company in stocks]

    plt.figure(figsize=(8, 6))
    plt.bar(tickers, market_caps)
    plt.title('Market Capitalization')
    plt.xlabel('Companies')
    plt.ylabel('Market Cap (in billions)')

def print_bubble_charts(stocks):
    tickers = [company['ticker'] for company in stocks]
    market_caps = [company['market_cap'] for company in stocks]
    revenues = [company['revenue'] for company in stocks]
    debts = [company['debt'] for company in stocks]
    pe_ratios = [company['pe_ratio'] for company in stocks]
    pb_ratios = [company['pb_ratio'] for company in stocks]
    ps_ratios = [company['ps_ratio'] for company in stocks]
    evt_ebitda_ratios = [company['evt_ebitda_ratio'] for company in stocks]
    
    bubble_sizes = [mc / 1e9 for mc in market_caps]
    
    plt.figure(figsize=(8, 6))
    plt.scatter(revenues, debts, s=bubble_sizes, alpha=0.5)

    plt.xlabel('Revenue')
    plt.ylabel('Debt')
    plt.title('Bubble Chart: Revenue vs Debt')

    for i in range(len(stocks)):
        plt.annotate(tickers[i], (revenues[i], debts[i]), ha='center', va='center')
        
    # ----------------------------------------------------------
    
    plt.figure(figsize=(8, 6))
    plt.scatter(pe_ratios, ps_ratios, s=bubble_sizes, alpha=0.5)

    plt.xlabel('P/E Ratio')
    plt.ylabel('P/S Ratio')
    plt.title('Bubble Chart: P/E Ratio vs P/S Ratio')

    for i in range(len(stocks)):
        plt.annotate(tickers[i], (pe_ratios[i], ps_ratios[i]), ha='center', va='center')
    
    # ----------------------------------------------------------
    
    plt.figure(figsize=(8, 6))
    plt.scatter(pb_ratios, evt_ebitda_ratios, s=bubble_sizes, alpha=0.5)

    plt.xlabel('P/B Ratio')
    plt.ylabel('EVT/EBITDA Ratio')
    plt.title('Bubble Chart: P/B Ratio vs EVT/EBITDA Ratio')

    for i in range(len(stocks)):
        plt.annotate(tickers[i], (pb_ratios[i], evt_ebitda_ratios[i]), ha='center', va='center')

def print_pie_charts(stocks):
    tickers = [company['ticker'] for company in stocks]
    assets = [company['assets'] for company in stocks]
    revenues = [company['revenue'] for company in stocks]
    debts = [company['debt'] for company in stocks]
    
    plt.figure(figsize=(8, 6))
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
    tickers = [company['ticker'] for company in stocks]
    ratios = [[company['pe_ratio'], company['pb_ratio'], company['ps_ratio'], company['evt_ebitda_ratio']] for company in stocks]

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

def print_heatmap_graphic(stocks):    
    filtered_data = [company for company in stocks if company['revenue'] > 30e9 and company['revenue'] < 1000e9]
    
    debt = np.array([company['debt'] for company in filtered_data]) / 1e9
    revenue = np.array([company['revenue'] for company in filtered_data]) / 1e9

    heatmap, xedges, yedges = np.histogram2d(debt, revenue, bins=14)

    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    plt.figure(figsize=(8, 6))
    plt.imshow(heatmap.T, origin='lower', cmap='coolwarm', extent=extent, aspect='auto')

    plt.colorbar(label='Number of Companies')
    plt.xlabel('Debt (in milliards)')
    plt.ylabel('Revenue (in milliards)')
    
    x_ticks = np.arange(min(debt), max(debt) + 1, 100)
    y_ticks = np.arange(min(revenue), max(revenue) + 1, 100)
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

    plt.title('Heatmap of Debt and Revenue Small sample')

def print_histogram_graphic(stocks):
    market_cap = [company['market_cap'] / 1000000000 for company in stocks]
    plt.figure(figsize=(8, 6))
    plt.hist(market_cap, bins=range(0,4000,20), edgecolor='black')
    plt.xlabel('Market Capitalization (in billions)')
    plt.ylabel('Number of Companies')
    plt.title('Histogram of Market Capitalization')

    # ----------------------------------------------------------

    plt.figure(figsize=(8, 6))
    plt.hist(market_cap, bins=range(0,200,7), edgecolor='black')
    plt.xlabel('Market Capitalization (in billions)')
    plt.ylabel('Number of Companies')
    plt.title('Histogram of Market Capitalization')

def print_scatter_graphic(stocks):
    assets = [company['assets'] / 1000000000 for company in stocks]
    cashflow = [company['cashflow'] / 1000000000 for company in stocks]
    
    plt.figure(figsize=(8, 6))
    plt.scatter(cashflow, assets, c='blue', alpha=0.5)
    plt.xlabel('CashFlow (in billions)')
    plt.ylabel('Assets (in billions)')
    plt.title('Scatter Plot of CashFlow vs. Assets')
    
    # ----------------------------------------------------------
    
    filtered_data = [company for company in stocks if  company['assets'] < 1000e9]

    assets = [company['assets'] / 1000000000 for company in filtered_data] 
    cashflow = [company['cashflow'] / 1000000000 for company in filtered_data]

    plt.figure(figsize=(8, 6))
    plt.scatter(cashflow, assets, c='blue', alpha=0.5)
    plt.xlabel('CashFlow (in billions)')
    plt.ylabel('Assets (in billions)')
    plt.title('Scatter Plot of CashFlow vs. Assets')
