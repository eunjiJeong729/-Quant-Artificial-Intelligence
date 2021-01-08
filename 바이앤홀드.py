import pandas as pd
import numpy as np
import matplotlib.pylab as plt

# read and index col 설정
df = pd.read_csv('SPY.csv', index_col='Date', parse_dates=['Date'])

print(df)
# 결측치
print(df[df.isin([np.nan, np.inf, -np.inf]).any(1)])

# 데이터 슬라이싱
price_df = df.loc[:,['Adj Close']].copy()
price_df.plot(figsize=(16,9))

from_date = '1997-01-03'
to_date = '2003-01-03'
price_df.loc[from_date:to_date].plot(figsize=(16,9))

# 일별 수익률
price_df['daily_rtn'] = price_df['Adj Close'].pct_change()
print(price_df.head(10))

# 누적곱
price_df['st_rtn'] = (1+price_df['daily_rtn']).cumprod()
print(price_df.head(10))

# 기준일 수익률
base_date = '2020-01-03'
tmp_df = price_df.loc[base_date:,['st_rtn']] / price_df.loc[base_date,['st_rtn']]
last_date = tmp_df.index[-1]
print('누적 수익 : ',tmp_df.loc[last_date,'st_rtn'])
tmp_df.plot(figsize=(16,9))
plt.show()