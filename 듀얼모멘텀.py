import pandas as pd
import numpy as np
import datetime

read_df = pd.read_csv('SPY.csv')
read_df.head()

price_df = read_df.loc[:,['Date', 'Adj Close']].copy()
price_df.head()

price_df['STD_YM'] = price_df['Date'].map(lambda x : datetime.datetime.strptime(x,'%Y-%m-%d').strftime('%Y-%m'))
print(price_df.head())

# 월말 종가
month_list = price_df['STD_YM'].unique()
month_last_df = pd.DataFrame()
for m in month_list :
    # 기준 연월에 맞는 인덱스의 마지막 날짜 row를 데이터프레임에 추가
    month_last_df = month_last_df.append(price_df.loc[price_df[price_df['STD_YM'] == m].index[-1],:])

month_last_df.set_index(['Date'],inplace=True)
print(month_last_df.head())

# 데이터 가공
month_last_df['BF_1M_Adj Close'] = month_last_df.shift(1)['Adj Close']
month_last_df['BF_2M_Adj Close'] = month_last_df.shift(12)['Adj Close']
month_last_df.fillna(0, inplace=True)
print(month_last_df.head(10))

# 포지션 기록
book = price_df.copy()
book.set_index(['Date'],inplace=True)
book['trade'] = ''
book.head()