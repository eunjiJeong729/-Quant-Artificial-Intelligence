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
month_last_df['BF_12M_Adj Close'] = month_last_df.shift(12)['Adj Close']
month_last_df.fillna(0, inplace=True)
print(month_last_df.head(10))

# 포지션 기록
book = price_df.copy()
book.set_index(['Date'],inplace=True)
book['trade'] = ''
book.head()

# 거래 실행
ticker = 'SPY' # trading
for x in month_last_df.index:
    signal = ''
    # 절대 모멘텀 계산
    momentum_index = month_last_df.loc[x, 'BF_1M_Adj Close'] / month_last_df.loc[x, 'BF_12M_Adj Close'] -1
    # 절대 모멘텀 지표 True / False 판단
    flag = True if ((momentum_index > 0.0) and (momentum_index != np.inf) and (momentum_index != -np.inf)) else False
    if flag :
        signal = 'buy' + ticker # 절대 모멘텀 지표가 Positive이면 매수 후 보유
    print('날짜 : ',x,' 모멘텀 인덱스 : ',momentum_index, 'flag : ',flag,'signal : ',signal)
    book.loc[x:, 'trade'] = signal

# 전략수익률
def returns(book, ticker):
    # 손익 계산
    rtn = 1.0
    book['return'] = 1
    buy = 0.0
    sell = 0.0
    for i in book.index:
        if book.loc[i, 'trade'] == 'buy ' + ticker and book.shift(1).loc[i, 'trade'] == '' :
            # long 진입
            buy = book.loc[i, 'Adj Close']
            print('진입일 : ',i, 'long 진입가격 : ',buy)
        elif book.loc[i, 'trade'] == 'buy ' + ticker and book.shift(1).loc[i, 'trade'] == 'buy ' + ticker :
            # 보유중
            current = book.loc[i, 'Adj Close']
            rtn = (current - buy) / buy + 1
            book.loc[i, 'return'] = rtn
        elif book.loc[i, 'trade'] == '' and book.shift(1).loc[i, 'trade'] == 'buy ' + ticker:
            # long 청산
            sell = book.loc[i, 'Adj Close']
            rtn = (sell - buy) / buy + 1 # 손익계산
            book.loc[i, 'return'] = rtn
            print('청산일 : ',i, 'long 진입가격 : ', buy, ' | long 청산가격 : ', sell, ' | return:', round(rtn, 4))
        if book.loc[i, 'trade'] == '': # 제로포지션
            buy = 0.0
            sell = 0.0
            current = 0.0
    acc_rtn = 1.0
    for i in book.index:
        if book.loc[i, 'trade'] == '' and book.shift(1).loc[i, 'trade'] == 'buy ' + ticker:
            # long 청산 시
            rtn = book.loc[i, 'return']
            acc_rtn = acc_rtn * rtn # 누적수익률
            book.loc[i:, 'acc return'] = acc_rtn

    print('Accunulated return :', round(acc_rtn, 4))
    return (round(acc_rtn, 4))

print(returns(book,ticker))