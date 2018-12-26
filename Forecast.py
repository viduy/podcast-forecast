import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import pymysql
from dateutil import parser
from datetime import timedelta
from datetime import datetime
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.stattools import acf, pacf


def test_stationarity(timeseries):
    #Determing rolling statistics
    ts_log = np.log(timeseries)
    # rolmean = pd.rolling_mean(timeseries, window=12)
    rolmean = ts_log.rolling(12).mean()
    # rolstd = pd.rolling_std(timeseries, window=12)
    rolstd = ts_log.rolling(12).std()
    plt.plot(timeseries, color='blue', label='Original')
    plt.plot(rolmean, color='red', label='Rolling Mean')
    plt.plot(rolstd, color='black', label='Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    # Perform Dickey-Fuller test:
    print('Results of Dickey-Fuller Test:')
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=[
                         'Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
    for key, value in dftest[4].items():
        dfoutput['Critical Value (%s)' % key] = value
    print(dfoutput)
    plt.show()

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
    dateList.sort(reverse=True)
    subList = []
    for i in range(1, len(dateList)):
        sub = dateList[i-1] - dateList[i]
        if int(sub.days) == 0:
            subList.append(1)
        else:
            subList.append(int(sub.days))
        
        
    subList.insert(0, int((datetime(2011, 1, 8) - datetime(2011, 1, 7)).days))
    cursor.close()
    connection.close()
    d = {'date': pd.Series(dateList),
         'updcycle': pd.Series(subList)}
    df = pd.DataFrame(d)
    # print(df.head())
    # print(df.dtypes)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    # print(df.index)
    ts = df['updcycle']
    ts_log = np.log(ts)
    # print(ts)
    # print(ts_log)
    ts_log_diff = ts_log - ts_log.shift()
    moving_avg = ts_log.rolling(12).mean()
    # moving_avg = pd.rolling_mean(ts_log, 12)
    # plt.plot(ts)

    # plt.plot(ts_log)
    # plt.plot(moving_avg, color='red')
    # ts_log_moving_avg_diff = ts_log - moving_avg
    # print(ts_log_moving_avg_diff.head(12))
    # ts_log_moving_avg_diff.dropna(inplace=True)
    # test_stationarity(ts_log_moving_avg_diff)
    expwighted_avg = ts_log.ewm(halflife=12).mean()

    # plt.plot(ts_log)
    # plt.plot(expwighted_avg, color='red')

    # ts_log_ewma_diff = ts_log - expwighted_avg
    # test_stationarity(ts_log_ewma_diff)
    # plt.plot(ts_log)
    # plt.show()

    # lag_acf = acf(expwighted_avg, nlags=20)
    # lag_pacf = pacf(expwighted_avg, nlags=20, method='ols')
    # #Plot ACF:
    # plt.subplot(121)
    # plt.plot(lag_acf)
    # plt.axhline(y=0, linestyle='--', color='gray')
    # plt.axhline(y=-1.96/np.sqrt(len(expwighted_avg)), linestyle='--', color='gray')
    # plt.axhline(y=1.96/np.sqrt(len(expwighted_avg)), linestyle='--', color='gray')
    # plt.title('Autocorrelation Function')
    # #Plot PACF:
    # plt.subplot(122)
    # plt.plot(lag_pacf)
    # plt.axhline(y=0, linestyle='--', color='gray')
    # plt.axhline(y=-1.96/np.sqrt(len(expwighted_avg)), linestyle='--', color='gray')
    # plt.axhline(y=1.96/np.sqrt(len(expwighted_avg)), linestyle='--', color='gray')
    # plt.title('Partial Autocorrelation Function')
    # plt.tight_layout()


    # model = ARIMA(ts_log, order=(2, 1, 0))
    # results_AR = model.fit(disp=-1)
    # plt.subplot(131)
    # plt.plot(ts_log_diff)
    # plt.plot(results_AR.fittedvalues, color='red')
    # plt.title('RSS: %.4f' % sum((results_AR.fittedvalues-ts_log_diff)**2))

    # model = ARIMA(ts_log, order=(0, 1, 2))  
    # results_MA = model.fit(disp=-1)  
    # plt.subplot(132)
    # plt.plot(ts_log_diff)
    # plt.plot(results_MA.fittedvalues, color='red')
    # plt.title('RSS: %.4f'% sum((results_MA.fittedvalues-ts_log_diff)**2))   

    model = ARIMA(ts_log, order=(2, 1, 2))
    results_ARIMA = model.fit(disp=-1)
    # plt.subplot(133)
    # plt.plot(ts_log_diff, color='blue')
    plt.plot(np.exp(results_ARIMA.fittedvalues)*10, color='red')
    # plt.title('RSS: %.4f' %
    #           sum((results_ARIMA.fittedvalues-ts_log_diff)**2))

    plt.tight_layout()

    predictions_ARIMA_diff = pd.Series(results_ARIMA.fittedvalues, copy=True)
    print (predictions_ARIMA_diff.head())

    predictions_ARIMA_diff_cumsum = predictions_ARIMA_diff.cumsum()
    print (predictions_ARIMA_diff_cumsum)

    predictions_ARIMA_log = pd.Series(ts_log.iloc[0], index=ts_log.index)
    predictions_ARIMA_log = predictions_ARIMA_log.add(
        predictions_ARIMA_diff_cumsum, fill_value=0)
    print(predictions_ARIMA_log)

    predictions_ARIMA = np.exp(predictions_ARIMA_log)
    plt.plot(ts)
    plt.plot(predictions_ARIMA)
    plt.title('RMSE: %.4f' % np.sqrt(sum((predictions_ARIMA-ts)**2)/len(ts)))


    # model = ARIMA(ts_log, order=(2, 1, 2))
    # results_ARIMA = model.fit(disp=-1)
    # # plt.plot(ts_log_diff)
    # # plt.plot(results_ARIMA.fittedvalues, color='red')
    # plt.title('RSS: %.4f' % sum((results_ARIMA.fittedvalues-ts_log_diff)**2))
    # predictions_ARIMA_diff = pd.Series(results_ARIMA.fittedvalues, copy=True)
    # print(predictions_ARIMA_diff.head())
    # predictions_ARIMA_diff_cumsum = predictions_ARIMA_diff.cumsum()
    # print(predictions_ARIMA_diff_cumsum.head())
    # predictions_ARIMA_log = pd.Series(ts_log.ix[0], index=ts_log.index)
    # predictions_ARIMA_log = predictions_ARIMA_log.add(
    #     predictions_ARIMA_diff_cumsum, fill_value=0)
    # print(predictions_ARIMA_log.head())
    # predictions_ARIMA = np.exp(predictions_ARIMA_log * 10)
    # plt.plot(ts)
    # plt.plot(predictions_ARIMA)
    # plt.title('RMSE: %.4f' % np.sqrt(sum((predictions_ARIMA-ts)**2)/len(ts)))
    plt.show()
    

inquirePublish('VoicerFM')
