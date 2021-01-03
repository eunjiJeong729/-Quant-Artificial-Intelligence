'''볼린저 밴드란 현재 주가가 상대적으로 높은지 낮은지 판단할 때 사용하는 보조지표임.
중심선인 이동평균, 상단 하단선인 표준편차로 총 3개선으로 구성됨.
'''

import pandas as pd
import matplotlib.pylab as plt

# S&P 500을 추종하는 ETF
df = pd.read_csv('SPY.csv')
print(df.head())

# 날짜와 수정종가를 추출
price_df = df.loc[:,['Date', 'Adj Close']].copy()
print(price_df.head())

# 중심선 만들기 rolling은 이동평균만드는 함수(20일)
price_df['center'] = price_df['Adj Close'].rolling(window=20).mean()
print(price_df.iloc[:])
price_df['ub'] = price_df['center'] + 2 * price_df['Adj Close'].rolling(window=20).std()
print(price_df.iloc[:])
price_df['lb'] = price_df['center'] - 2 * price_df['Adj Close'].rolling(window=20).std()
print(price_df.iloc[:])

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
base_data = '2019-12-01'
sample = bollinger.loc[base_data:]
print(sample.head())

# 진입 또는 청산 신호 발생 시 기록(거래장부) 생성
book = sample[['Date', 'Adj Close']].copy()
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
        elif sample.loc[i, 'ub'] >= sample.loc[i, 'Adj Close'] and sample.loc[i, 'Adj Close'] >= sample.loc[i,'lb']: # 볼린저 밴드 안에 있으면
            if book.shift(1).loc[i, 'trade'] == 'buy': # 이미 매수이면
                book.loc[i, 'trade'] = 'buy' # 유지
            else :
                book.loc[i, 'trade'] = ''  # 동작 안함
    return book

book = tradings(sample, book)
print(book.tail(10))
book = book.set_index('Date')

# 전략수익률

def rate_returns(book) :
    rtn = 1.0
    book['return'] = 1
    buy = 0.0
    sell = 0.0
    for i in book.index:
        # long 진입(매수 신호가 있을 경우)
        if book.loc[i, 'trade'] == 'buy' and book.shift(1).loc[i, 'trade'] == '':
            buy = book.loc[i, 'Adj Close']
            print('진입일 : ', i, 'long 진입가격 : ', buy)
        # long 청산(매도 신호가 있을 경우)
        elif book.loc[i, 'trade'] == '' and book.shift(1).loc[i, 'trade'] == 'buy':
            sell = book.loc[i, 'Adj Close']
            rtn = (sell - buy) / buy + 1 # 손익계산
            book.loc[i, 'return'] = rtn # 수익률 저장
            print('청산일 : ', i, 'long 진입가격 : ', buy, ' | long 청산가격 : ', sell, ' | return : ', round(rtn, 4))

        if book.loc[i, 'trade'] == '': # 제로
            buy = 0.0
            sell = 0.0
    acc_rtn = 1.0
    for i in book.index:
        rtn = book.loc[i, 'return']
        acc_rtn = acc_rtn * rtn # 누적 수익률
        book.loc[i, 'acc return'] = acc_rtn
    print('Accunulated return : ', round(acc_rtn, 4))
    return round(acc_rtn, 4)

print(rate_returns(book))

# 변화추이
book['acc return'].plot()
plt.show()