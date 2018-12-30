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

@app.route('/forecast')
def forecast():
    return render_template('forecast.html')

@app.route('/search/epList', methods = ['GET'])
def epList():
    if not request.args.get('title'):  # 檢測是否有數據
        return jsonify({'code': 1, 'msg': 'no par'})
    
    title = request.args.get('title')
    print(title)
    connection = pymysql.connect(host='localhost', user='root',
                                 passwd='iX2yPaDJYjPAQn', db='podcast', port=3306, charset='utf8')
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute('select rssUrl from rss where feedTitle REGEXP %s', title)
    rssUrl = cursor.fetchone()
    # dataMany = cursor.fetchmany(3)
    if not rssUrl:
        return jsonify({'code': 1, 'msg': 'no resutlt'})
    print(rssUrl)
    cursor.execute('update rss set hot = hot + 1 where rssUrl = %s', rssUrl['rssUrl'])
    cursor.execute('select * from episode where rssUrl = %s', rssUrl['rssUrl'])
    data = cursor.fetchall()
    # print(data)
    for i in range(0, len(data)):
        # print(data[i]['date'])
        data[i]['date'] = parser.parse(str(data[i]['date']))
    # print(str(data))
    # print(data)
    data = sorted(data, key=lambda k: k['date'], reverse=True)
    cursor.close()
    connection.commit()
    connection.close()
    return jsonify({'code': 0, 'msg': 'ok', 'data': data})


@app.route('/search/like', methods=['GET'])
def likeList():
    print('nothing')

@app.route('/action/like')
def like():
    if not request.args.get('rss1'):  # 檢測是否有數據
        return jsonify({'code': 1, 'msg': 'missing par'})
    if not request.args.get('rss2'):
        return jsonify({'code': 1, 'msg': 'missing par'})
    rss1 = request.args.get('rss1')
    rss2 = request.args.get('rss2')

if __name__ == '__main__':
    app.run()
