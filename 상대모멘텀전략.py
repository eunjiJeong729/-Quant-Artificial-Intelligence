import os
import glob
import pandas as pd
import numpy as np
import datetime

# 종목 데이터 읽기
files = glob.glob('*.csv')

# Monthly 데이터 저장
month_last_df = pd.DataFrame(columns=['Date','CODE','1M_RET'])
#종목 데이터프레임 생성
stock_df = pd.DataFrame(columns=['Date','CODE','Adj Close'])

def data_preprocessing(samlpe, ticker, base_date):
    samlpe['CODE'] = ticker # 종목 코드 추가
    samlpe = samlpe[samlpe['Date'] >= base_date][['Date','CODE','Adj Close']].copy()
    # 기준일자 이후 데이터 사용
    samlpe.reset_index(inplace= True, drop= True)
    samlpe['STD_YM'] = samlpe['Date'].map(lambda x : datetime.datetime.strptime(x, '%Y-%m-%d').strftime('%Y-%m')) # 기준년월
    samlpe['1M_RET'] = 0.0 # 수익률 컬럼
    ym_keys = list(samlpe['STD_YM'].unique()) # 중복 제거한 기준년월 목록
    return samlpe, ym_keys

for file in files :
    '''
    데이터 저장 경로에 있는 개별 종목들을 읽어옴
    '''
    if os.path.isdir(file):
        print('%s <DIR> '%file)
    else:
        folder, name = os.path.split(file)
        head, tail = os.path.splitext(name)
        print(file)
        read_df = pd.read_csv(file)
        # 데이터 가공
        price_df, ym_keys = data_preprocessing(read_df,head,base_date='2019-12-12')