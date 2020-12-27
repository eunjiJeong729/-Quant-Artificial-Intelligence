'''볼린저 밴드란 현재 주가가 상대적으로 높은지 낮은지 판단할 때 사용하는 보조지표임.
중심선인 이동평균, 상단 하단선인 표준편차로 총 3개선으로 구성됨.
'''

import pandas as pd
# S&P 500을 추종하는 ETF
df = pd.read_csv('SPY.csv')
print(df.head())

# 날짜와 수정종가를 추출
price_df = df.loc[:,['Date', 'Adj Close']].copy()
print(price_df.head())

# 중심선 만들기 rolling은 이동평균만드는 함수(20일)
price_df['center'] = price_df['Adj Close'].rolling(window=20).mean()
print(price_df.iloc[13:25])
price_df['ub'] = price_df['center'] + 2 * price_df['Adj Close'].rolling(window=20).std()
print(price_df.iloc[13:25])
price_df['lb'] = price_df['center'] - 2 * price_df['Adj Close'].rolling(window=20).std()
print(price_df.iloc[13:25])

n = 20
sigma = 2
def bollinger_band(price_df, n, sigma) :
    bb = price_df.copy()
    # 중심선 만들기(이동평균선)
    bb['center'] = price_df['Adj Close'].rolling(window=20).mean()
    # 상하단선 만들기
    bb['ub'] = price_df['center'] + 2 * price_df['Adj Close'].rolling(window=20).std()
    bb['lb'] = price_df['center'] - 2 * price_df['Adj Close'].rolling(window=20).std()
    return bb

# 볼린저 밴드를 사용한 전략 성과 확인
bollinger = bollinger_band(price_df, n, sigma)
base_data = '2020-01-01'
sample = bollinger.loc[base_data:]
print(sample.head())

# 진입 또는 청산 신호 발생 시 기록(거래장부) 생성
book = sample[['Adj Close']].copy()
book['trade'] = ''