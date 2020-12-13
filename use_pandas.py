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

# 슬라이싱, 인덱싱
slice_df = df[['Open', 'High']].head()
print(slice_df[:2])
print(df['2020-12-01':'2020-12-10']) # use index col

df['Close_lag'] = df['Close'].shift() # 전일자 연결(시계열)
df['close_pac'] = df['Close'].pct_change() # 수익률
df['close_diff'] = df['Close'].diff() # 변화량
df['MA'] = df['Close'].rolling(window=5).mean() # 이동평균선
print(df.head(10))

# resample 기간 조정
index = pd.date_range(start= '2020-01-01', end= '2020-12-01', freq='B') # 영업일
series = pd.Series(range(len(index)), index=index)
print(series)
series.resample(rule='M').sum() # 월 합계
series.resample(rule='M').last() # 매월 마지막 영업일
series.resample(rule='MS').first() # 매월 1영업일
