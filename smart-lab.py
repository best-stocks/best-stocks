import requests
import pandas as pd
import os

name_plus = '.csv'
indexes = {0: 'revenue', 1:'cashflow', 2:'assets',
           3:'current_assets', 4:'debt',5:'current_price',
           6:'shares_outstanding', 7:'market_cap', 8:'pe_ratio',
           9:'ps_ratio', 10:'pb_ratio', 11:'evt_ebitda_ratio'}

multiplicate = {0:1_000_000_000,1:1_000_000_000,2:1_000_000_000,
                3:1_000_000_000,4:1_000_000_000,5:1,6:1_000_000,
                7:1_000_000_000,8:1,9:1 ,10:1,11:1}


def download_by_tiker(company_tiker):
    url = f'https://smart-lab.ru/q/{company_tiker}/f/y/MSFO/download/'
    r = requests.get(url)
    if(r.status_code == 200):
        file = open(f"{company_tiker}.csv", "wb")
        file.write(r.content)
        print(company_tiker)
    else:
        print('tiker is wrong')

def get_values_by_tiker(data_base_file, tiker):
    df = pd.read_csv(data_base_file)
    df = df.rename(index=indexes)
    dict_of_val = df[tiker].to_dict()
    i = 0
    for key in dict_of_val:
        val = dict_of_val[key].replace(" ", "")
        val = float(val) * multiplicate[i]
        dict_of_val[key] = val
        i += 1
    return dict_of_val

def make_data(tiker_file_name, year, output_file):
    tiker_file = open(tiker_file_name, 'r')
    tikers = tiker_file.read().split('\n')
    df_main = pd.DataFrame({'Unnamed: 0': ["Выручка, млрд руб",
                                           "Операционный денежный поток, млрд руб",
                                           "Активы, млрд руб", "Чистые активы, млрд руб", "Долг, млрд руб",
                                           "Цена акции ао, руб", "Число акций ао, млн",
                                           "Капитализация, млрд руб",
                                           "P/E", "P/S", "P/BV", "EV/EBITDA"], 'del': [0]*12})
    start = True
    for tiker in tikers:
        if(tiker == ''):
            continue
        download_by_tiker(tiker)
        tmp_df = pd.read_csv(tiker + name_plus, sep=';')
        for columnIn in tmp_df:
            if(columnIn != year and columnIn != "Unnamed: 0"):
                tmp_df = tmp_df.drop(columns=columnIn)
        if(tmp_df.shape[1] == 1):
            os.remove(tiker + name_plus)
            continue
        tmp_df.rename(columns={year:tiker}, inplace=True)
        df_main = df_main.merge(tmp_df, on='Unnamed: 0', how='left')
        if(start):
            df_main = df_main.drop(df_main.columns[1], axis=1)
            start = False
        os.remove(tiker + name_plus)

    null_counter = df_main.isnull().sum()
    for column in df_main.columns:
        if(null_counter[column] > 0):
            df_main = df_main.drop(columns=column)
    df_main = df_main.drop(df_main.columns[0], axis=1)
    df_main.to_csv (rf'C:\Users\danul\PyhonMathlab\Data\{output_file}', index= False )