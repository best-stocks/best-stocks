# best-stocks
**==best-stocks==** is a service for finding undervalued stocks on the Russian and US markets. The service is completely free and helps find stocks that will grow in the medium term based on fundamentals. The sample size is 90 stocks for the US market and a maximum of 230 stocks for the Russian market, but this value is different for each year

To update and retrieve data from the US market we use api [alphavintage](https://www.alphavantage.co/), for the free api key there is a limit of 5 requests per minute and 500 requests per day, getting the api key takes ~2 min

Service [smartlab](https://smart-lab.ru/) is used to get data for different years from Russian market. It is possible to collect stock data for different years.

Datasets are automatically created in the program from the number of available stocks for the selected market. All available stocks for the Russian market can be seen in `tickers/en/ru_tickers.txt`, for the American market - in `tickers/en/top90.txt`. Datasets are created in the folders `dataset/en` and `dataset/en` respectively

Ratios `pe_ratio`, `ps_ratio`, `pb_ratio` and others are used to evaluate shares, a total of 8 fundamental ratios. Each share is given its own weight, depending on the value of the corresponding coefficient, at the very end the share with the highest score on all the coefficients is looked for first, and then when the shares are equal, the number of trials they beat is evaluated

The names of datasets, cached tickers and so on can be changed in the `constants.py` module

### Quickstart
-------------------------------------------
First create a file `.env` and write `API_KEY = 'YOUR_KEY'` there, where `YOUR_KEY` is your api key, which can be obtained from [alphavintage](https://www.alphavantage.co/support/#api-key)

You can see an example in `.env.example`.

Also, to install all packages used by the program, write in the root of the project:
```bash
pip install -r requirements.txt
```

**Then you are free to use the program!

To **run** it, type at the root of the project: 
```bash
python3 main.py
```

### Dependencies
-------------------------------------------
**For requests:**
- [requests](https://pypi.org/project/requests/)

**For working with .env files:**
- [python-dotenv](https://pypi.org/project/python-dotenv/)

**For generating a nice bootstrap scale:**
- [tqdm](https://pypi.org/project/tqdm/)

**For working with data and graphs:**
- [pandas](https://pandas.pydata.org/)
- [matplotlib](https://matplotlib.org/)
- [numpy](https://numpy.org/)

### Licence
-------------------------------------------
**Licensed under:**
- MIT license ([LICENSE-MIT](https://github.com/seanmonstar/httparse/blob/master/LICENSE-MIT) or [https://opensource.org/licenses/MIT](https://opensource.org/licenses/MIT))