import pandas as pd
import numpy as np
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