import matplotlib.pyplot as plt
import pymysql
import time
from dateutil import parser
from datetime import timedelta
from datetime import datetime

x = []
y = []


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
    print(dateList)
    isFirst = True
    for j in range(1, 100):
        averge = datetime(2011, 1, 7) - datetime(2011, 1, 7)
        listRange = j * 10
        if listRange > len(dateList):
            if not isFirst:
                break
            print('overflow')
            isFirst = False
            listRange = len(dateList)
        for i in range(1, listRange):
            averge += dateList[i - 1] - dateList[i]
        print(listRange)
        print(averge / (listRange - 1))
        y.append((averge / (listRange - 1)).days)
        x.append(j * 10)
    cursor.close()
    connection.close()
    plt.plot(x, y, label="chart", marker='o', color="red",
             linestyle='--', markerfacecolor='b')
    plt.xlabel('Cricle')
    plt.ylabel('Date')
    plt.title(' Averge Publish')
    plt.legend()
    plt.savefig("chart/" + title + " Chart.png", dpi=400)
    plt.show()


inquirePublish('大内密谈')
