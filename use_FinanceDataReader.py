import FinanceDataReader as fdr
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = 'eunji'
plt.rcParams["figure.figsize"] = (14,4)
plt.rcParams['lines.linewidth'] = 2
plt.rcParams["axes.grid"] = True

# 종목 list
# 한국거래소 상장종목 전체
df_krx = fdr.StockListing('KRX')
df_krx.head()
print(df_krx)

# 나스닥 종목 전체
df_spx = fdr.StockListing('NASDAQ')
print(df_spx.head())

# 가격데이터 한국, 6자리 종목코드
# 신라젠, 2020년
df = fdr.DataReader('215600', '2020')
print(df.head(10))

# 셀트리온, 2017년~현재
df = fdr.DataReader('068270', '2017')
df['Close'].plot()
plt.show() # 이미지 출력

# 가격데이터 미국, ticker명
# 애플(AAPL), 2020-01-01 ~ 2020-03-30
df = fdr.DataReader('AAPL', '2020-01-01', '2020-03-30')
print(df.tail())

# 국가별 지수 PLOT 차트
# KS11 (KOSPI 지수), 2015년~현재
df = fdr.DataReader('KS11', '2015')
print(df['Close'].plot())

# 다우지수, 2015년~현재
df = fdr.DataReader('DJI', '2015')
print(df['Close'].plot())

# 환율
# 원달러 환율, 1995년~현재
df = fdr.DataReader('USD/KRW', '1995')
print(df['Close'].plot())

# 위엔화 환율, 1995년~현재
df = fdr.DataReader('CNY/KRW', '1995')
print(df['Close'].plot())