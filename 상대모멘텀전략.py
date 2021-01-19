import os
import glob
import pandas as pd
import numpy as np
import datetime

# 종목 데이터 읽기
files = glob.glob('SPY.csv')

# Monthly 데이터 저장
month_last_df = pd.DataFrame(columns=['Date','CODE','1M_RET'])
#종목 데이터프레임 생성
stock_df = pd.DataFrame(columns=['Date','CODE','Adj Close'])