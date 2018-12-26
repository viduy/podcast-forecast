import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import pymysql
from dateutil import parser
from datetime import timedelta
from datetime import datetime
from statsmodels.tsa.stattools import adfuller
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.stattools import acf, pacf


def inquirePublish(title):
    connection = pymysql.connect(host='localhost', user='root',
                                 passwd='iX2yPaDJYjPAQn', db='podcast', port=3306, charset='utf8')
    cursor = connection.cursor()
    cursor.execute('select rssUrl from rss where feedTitle = %s', title)
    rssUrl = cursor.fetchone()
    print(rssUrl)
    cursor.execute('select date from episode where rssUrl = %s', rssUrl)
    date = cursor.fetchall()
    dateList = []
    for item in date:
        dt = parser.parse(str(item[0]))
        dateList.append(dt)
    dateList.sort(reverse=False)
    # for i in range(1, len(dateList)):
    #     sub = dateList[i-1] - dateList[i]
    #     if int(sub.days) == 0:
    #         subList.append(1)
    #     else:
    #         subList.append(int(sub.days))
    subList = []
    indexList = []
    i = dateList[0]
    j = 0
    while i <= dateList[-1]:
        if abs((dateList[j] - i).days) < 1:
            j = j + 1
        if j == len(dateList):
            break
        sub = dateList[j] - i
        subList.append(sub.days)
        indexList.append(i)
        i = i + timedelta(days=1)
    # subList.insert(0, int((datetime(2011, 1, 8) - datetime(2011, 1, 7)).days))
    # dateList.pop(1)
    cursor.close()
    connection.close()
    print(dateList)
    d = {'index': pd.Series(indexList),
         'sub': pd.Series(subList)}
    df = pd.DataFrame(d)
    print(df)
    # print(df.dtypes)
    # df['sub'] = pd.to_datetime(df['date'])
    # df.set_index('date', inplace=True)
    # print(df)
    # # print(df.index)
    ts = df['sub']
    ts_log = np.log(ts)
    # test_stationarity(ts)
    print(test_stochastic(ts))
    

# def test_stationarity(timeseries):
#     #Determing rolling statistics
#     ts_log = np.log(timeseries)
#     # rolmean = pd.rolling_mean(timeseries, window=12)
#     rolmean = ts_log.rolling(12).mean()
#     # rolstd = pd.rolling_std(timeseries, window=12)
#     rolstd = ts_log.rolling(12).std()
#     plt.plot(timeseries, color='blue', label='Original')
#     plt.plot(rolmean, color='red', label='Rolling Mean')
#     plt.plot(rolstd, color='black', label='Rolling Std')
#     plt.legend(loc='best')
#     plt.title('Rolling Mean & Standard Deviation')
#     # Perform Dickey-Fuller test:
#     print('Results of Dickey-Fuller Test:')
#     dftest = adfuller(timeseries, autolag='AIC')
#     dfoutput = pd.Series(dftest[0:4], index=[
#                          'Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
#     for key, value in dftest[4].items():
#         dfoutput['Critical Value (%s)' % key] = value
#     print(dfoutput)
#     plt.show()


def test_stationarity(timeseries):
    dftest = adfuller(timeseries, autolag='AIC')
    return dftest[1]


def test_stochastic(ts):
    p_value = acorr_ljungbox(ts, lags=1)[1]  # lags可自定义
    return p_value
inquirePublish('VoicerFM')
