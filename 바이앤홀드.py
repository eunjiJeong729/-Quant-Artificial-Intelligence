import pandas as pd
import numpy as np
# read and index col 설정
df = pd.read_csv('SPY.csv', index_col='Date', parse_dates=['Date'])

# 결측치
print(df[df.isin([np.nan, np.inf, -np.inf]).any(1)])