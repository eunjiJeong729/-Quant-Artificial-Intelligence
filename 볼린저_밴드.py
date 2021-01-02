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

# 거래전략
''' 가정 : 현재 주가가 일정기간 평균가격 보다 낮다 --> 가격상승 예상(매수)
           현재 주가가 일정기간 평균가격 보다 높다 --> 가격하락 예상(매도)
           20일 이동 평균선을 사용, 유의수준 5%
'''
def tradings(sample,book):
    for i in sample.index:
        if sample.loc[i, 'Adj Close'] > sample.loc[i, 'ub'] : # 상단 이탈 시 동작 안함
            book.loc[i, 'trade'] = ''
        elif sample.loc[i, 'lb'] > sample.loc[i, 'Adj Close'] : # 하단 이탈 시 매수
            if book.shift(1).loc[i, 'trade'] == 'buy': # 이미 매수이면
                book.loc[i, 'trade'] = 'buy' # 유지
            else :
                book.loc[i, 'trade'] = 'buy'  # 매수
        elif sample.loc[i, 'ub'] > sample.loc[i, 'Adj Close'] and sample.loc[i, 'Adj Close'] >= sample.loc[i,'lb']: # 볼린저 밴드 안에 있으면
            if book.shift(1).loc[i, 'trade'] == 'buy': # 이미 매수이면
                book.loc[i, 'trade'] = 'buy' # 유지
            else :
                book.loc[i, 'trade'] = ''  # 동작 안함
    return book

book = tradings(sample, book)
print(book.tail(10))