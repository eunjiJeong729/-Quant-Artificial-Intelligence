import datetime
import pandas as pd

# strptime str to datetime
format = '%Y-%m-%d %H:%M:%S'
date_str = '2020-12-10 23:26:01'
date_dt = datetime.datetime.strptime(date_str, format)
print(type(date_dt))

# strftime datetime to str
date_str = date_dt.strftime('%Y-%m-%d %H:%M:%S')
print(type(date_str))
  # 형식 변환
date_str2 = date_dt.strftime('%Y-%m-%d %H')
print(date_str2)

# date time use pandas
# Timestamp 현재까지의 시간 계산
pd.Timestamp(1239.1238934, unit = 'D')
untill_sysdate = pd.Timestamp('2019-1-1')
pd.to_datetime('2019-1-1 12')
pd.to_datetime(['2018-1-1', '2019-1-2'])
# date_range 자동 날짜 생성
date_li = pd.date_range('2020-01', '2020-02', freq='B')
print(date_li)
# Time spans 기간 계산
pd.Period('2020-01')
# freq로 기간 조정
pd.Period('2020-02', freq = 'D')
date_li = pd.period_range('2020-01', '2020-02', freq='D')
print(date_li)