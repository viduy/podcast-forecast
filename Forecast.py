import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import pymysql
# %matplotlib inline
from dateutil import parser
from datetime import timedelta
from datetime import datetime


def inquirePublish(title):
    connection = pymysql.connect(host='localhost', user='root',
                                 passwd='iX2yPaDJYjPAQn', db='podcast', port=3306, charset='utf8')
    cursor = connection.cursor()
    cursor.execute('select rssUrl from rss where feedTitle = %s', title)
    rssUrl = cursor.fetchone()
    # dataMany = cursor.fetchmany(3)
    print(rssUrl)
    cursor.execute('select date from episode where rssUrl = %s', rssUrl)
    date = cursor.fetchall()
    dateList = []
    for item in date:
        # print(item)
        dt = parser.parse(str(item[0]))
        # print(str(item[0]))
        # print(dt)
        dateList.append(dt)
        # cursor.execute('select ')
    dateList.sort(reverse=True)
    # print(dateList)
    # isFirst = True
    subList = []
    # for j in range(1, 100):
        # averge = datetime(2011, 1, 7) - datetime(2011, 1, 7)
        # listRange = j * 10
        # if listRange > len(dateList):
        #     if not isFirst:
        #         break
        #     print('overflow')
        #     isFirst = False
        #     listRange = len(dateList)
        # for i in range(1, listRange):
        #     subList.append(dateList[i - 1] - dateList[i])
            # averge += dateList[i - 1] - dateList[i]
        # print(listRange)
        # print(averge / (listRange - 1))
    for i in range(1, len(dateList)):
        subList.append(dateList[i-1] - dateList[i])
    subList.insert(0, datetime(2011, 1, 7) - datetime(2011, 1, 7))
    cursor.close()
    connection.close()
    d = {'date': pd.Series(dateList),
         'updcycle': pd.Series(subList)}
    df = pd.DataFrame(d)
    print(df.head())
    print(df.dtypes)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df.index
    ts = df['updcycle']
    print(ts)
    plt.plot(ts)
    plt.legend()
    # plt.savefig("Chart.png", dpi=400)
    plt.show()


inquirePublish('Anyway.FM 设计杂谈')

