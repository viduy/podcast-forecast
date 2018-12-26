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
import statsmodels.api as sm
from statsmodels.graphics.api import qqplot

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
    dateList = dateList[-10:-1]
    print(dateList)
    subList = []
    indexList = []
    i = dateList[0]
    j = 0
    while i <= dateList[-1]:
        if abs((dateList[j] - i).days) < 1:
            j = j + 1
        if j == len(dateList):
            print(len(dateList))
            break;
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
    dta = df['sub']
    # arma_mod20 = sm.tsa.ARMA(dta, (7, 0)).fit()

    arma_mod20 = sm.tsa.ARMA(dta, (7, 0)).fit()
    # print(arma_mod20.aic, arma_mod20.bic, arma_mod20.hqic)
    # print(sm.stats.durbin_watson(arma_mod20.resid.values))
    # arma_mod30 = sm.tsa.ARMA(dta, (0, 1)).fit()
    # print(arma_mod30.aic, arma_mod30.bic, arma_mod30.hqic)
    # print(sm.stats.durbin_watson(arma_mod30.resid.values))
    # arma_mod40 = sm.tsa.ARMA(dta, (7, 1)).fit()
    # print(arma_mod40.aic, arma_mod40.bic, arma_mod40.hqic)
    # print(sm.stats.durbin_watson(arma_mod40.resid.values))
    # arma_mod50 = sm.tsa.ARMA(dta, (8, 0)).fit()
    # print(arma_mod50.aic, arma_mod50.bic, arma_mod50.hqic)
    # print(sm.stats.durbin_watson(arma_mod50.resid.values))



    # fig = plt.figure(figsize=(12, 8))

    predict_sunspots = arma_mod20.predict(
        start=90, end=140, dynamic=True)
    print(predict_sunspots)
    plt.figure(figsize=(12, 8))
    # ax3 = fig.add_subplot(713)
    # predict_sunspots.plot(ax=ax3)
    predict_sunspots.plot()
    dta.plot()
    plt.legend(loc='best')
    plt.show()


inquirePublish('VoicerFM')

