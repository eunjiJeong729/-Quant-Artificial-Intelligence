import datetime

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