from flask import Flask, render_template  # 导入Flask包
from flask import Flask
from flask import request
from flask import redirect
from flask import jsonify
import json
import pymysql
from dateutil import parser
from datetime import timedelta
from datetime import datetime

app = Flask(__name__)  # 获取Flask对象，以当前模块名为参数


# 路由默认为（127.0.0.1:5000）
@app.route('/',)  # 装饰器对该方法进行路由设置，请求的地址
def index():  # 方法名称
    return render_template('index.html')# 返回响应的内容

@app.route('/search', methods = ['GET'])
def search():
    if not request.data:  # 檢測是否有數據
        return jsonify({'code': 1})
    
    data = request.data.decode('utf-8')
    data_json = json.loads(data)
    title = data_json['title']
    connection = pymysql.connect(host='localhost', user='root',
                                 passwd='iX2yPaDJYjPAQn', db='podcast', port=3306, charset='utf8')
    cursor = connection.cursor()
    cursor.execute('select rssUrl from rss where feedTitle = %s', title)
    rssUrl = cursor.fetchone()
    # dataMany = cursor.fetchmany(3)
    print(rssUrl)
    cursor.execute('select * from episode where rssUrl = %s', rssUrl)
    data = cursor.fetchall()
    # dateList = []
    for item in data:
        print(item[len(item)-1])
        dt = parser.parse(str(item['date']))
        # print(str(item[0]))
        # print(dt)
        
        # cursor.execute('select ')
    # dateList.sort(reverse=True)
    cursor.close()
    connection.close()
    return jsonify({'code': 0, 'data': data})


if __name__ == '__main__':
    app.run()
