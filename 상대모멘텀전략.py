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