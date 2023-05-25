import matplotlib.pyplot as plt

tickers = []
pe_ratios = []
pb_ratios = []
ps_ratios = []
market_caps = []
volumes = []

def set_data(stocks):
    for stock in stocks:
        tickers.append(stock['ticker'])
        pe_ratios.append(stock['pe_ratio'])
        pb_ratios.append(stock['pe_ratio'])
        ps_ratios.append(stock['pe_ratio'])
        market_caps.append(stock['market_cap'])
        volumes.append(stock['volume'])

def print_charts(stocks):
    set_data(stocks=stocks)

    plt.figure(1)
    plt.subplot(1, 2, 1)
    plt.bar(tickers, market_caps)
    plt.title('Market Capitalization')
    plt.xlabel('Companies')
    plt.ylabel('Market Cap (in billions)')
    
    plt.subplot(1, 2, 2)
    plt.pie(volumes, labels=tickers, autopct='%1.1f%%')
    plt.title('Volume')
    
    plt.figure(2)
    plt.subplot(1, 3, 1)
    plt.scatter(market_caps, pe_ratios, s=100, alpha=0.5)
    plt.title('Market Cap vs. P/E Ratio')
    plt.xlabel('Market Cap (in billions)')
    plt.ylabel('P/E Ratio')
    
    plt.subplot(1, 3, 2)
    plt.scatter(market_caps, pe_ratios, s=100, alpha=0.5)
    plt.title('Market Cap vs. P/E Ratio')
    plt.xlabel('Market Cap (in billions)')
    plt.ylabel('P/E Ratio')
    
    plt.subplot(1, 3, 3)
    plt.scatter(market_caps, pe_ratios, s=100, alpha=0.5)
    plt.title('Market Cap vs. P/E Ratio')
    plt.xlabel('Market Cap (in billions)')
    plt.ylabel('P/E Ratio')
    
    plt.tight_layout()
    plt.show()
