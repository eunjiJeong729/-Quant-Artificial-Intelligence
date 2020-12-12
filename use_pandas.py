import pandas as pd
# read and index col 설정
df = pd.read_csv('SPY.csv', index_col='Date', parse_dates=['Date'])
print(df.head())
print(type(df.index))
print(df.index[0])

# 결측치, 이상치 제거
print(df.isna().sum()) # 확인
df.fillna(0) # null -> 0
df.fillna(df.mean()), df.where(pd.notnull(df), df.mean(), axis='columns') # null -> 각 col별 mean
df.dropna(axis = 0) # null -> row del
