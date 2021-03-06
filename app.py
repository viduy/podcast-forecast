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
from datetime import timezone
import pytz

app = Flask(__name__)  # 获取Flask对象，以当前模块名为参数


# 路由默认为（127.0.0.1:5000）
@app.route('/',)  # 装饰器对该方法进行路由设置，请求的地址
def index():  # 方法名称
    return render_template('index.html')# 返回响应的内容

@app.route('/search/reload', methods=['GET'])
def reload():
    if not request.args.get('rss'):  # 檢測是否有數據
        return jsonify({'code': 1, 'msg': 'no par'})

    rssUrl = {'rssUrl': request.args.get('rss')}
    print(rssUrl)
    connection = pymysql.connect(host='localhost', user='root',
                                 passwd='iX2yPaDJYjPAQn', db='podcast', port=3306, charset='utf8')
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    # cursor.execute('select rssUrl from rss where feedTitle REGEXP %s', title)
    # rssUrl = cursor.fetchone()
    # # dataMany = cursor.fetchmany(3)
    # if not rssUrl:
    #     return jsonify({'code': 1, 'msg': 'no resutlt'})
    # print(rssUrl)
    cursor.execute(
        'update rss set hot = hot + 1 where rssUrl = %s', rssUrl['rssUrl'])
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
    return jsonify({'code': 0, 'msg': 'ok', 'data': data, 'rss': rssUrl['rssUrl']})

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
    return jsonify({'code': 0, 'msg': 'ok', 'data': data, 'rss': rssUrl['rssUrl']})


@app.route('/search/reload/like', methods=['GET'])
def reLikeList():
    if not request.args.get('rss'):  # 檢測是否有數據
        return jsonify({'code': 1, 'msg': 'no par'})

    rssUrl = {'rssUrl':request.args.get('rss')}
    print(rssUrl)
    connection = pymysql.connect(host='localhost', user='root',
                                 passwd='iX2yPaDJYjPAQn', db='podcast', port=3306, charset='utf8')
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute('select rss2, con from con where rss1 = %s',
                   rssUrl['rssUrl'])
    result = cursor.fetchall()
    data = []
    if not result:
        print('no result')

    else:
        for item in result:
            format = {'rss': '', 'con': 1}
            format['rss'] = item['rss2']
            format['con'] = item['con']
            data.append(format)
    cursor.execute('select rss1, con from con where rss2 = %s',
                   rssUrl['rssUrl'])
    result2 = cursor.fetchall()
    print(result2)
    if not result2:
        print('no resutlt2')
    else:
        for item in result2:
            format = {'rss': '', 'con': 1}
            format['rss'] = item['rss1']
            format['con'] = item['con']
            data.append(format)
    dataSend = []
    for i in range(0, len(data)):
        format = {'feedTitle': '', 'feedLink': '',
                  'img': '', 'con': 1, 'rssUrl': ''}
        cursor.execute('select * from rss where rssUrl = %s', data[i]['rss'])
        result3 = cursor.fetchone()
        print('final')
        if not result3:
            print('no result3')
        else:
            format['feedTitle'] = result3['feedTitle']
            format['feedLink'] = result3['feedLink']
            format['img'] = result3['img']
            format['rssUrl'] = result3['rssUrl']
            format['con'] = data[i]['con']
            dataSend.append(format)
    dataSend = sorted(dataSend, key=lambda k: k['con'], reverse=True)
    print(dataSend)
    return jsonify({'code': 0, 'msg': 'ok', 'data': dataSend})


@app.route('/search/like', methods=['GET'])
def likeList():
    if not request.args.get('title'):  # 檢測是否有數據
        return jsonify({'code': 1, 'msg': 'no par'})

    title = request.args.get('title')
    print(title)
    connection = pymysql.connect(host='localhost', user='root',
                                 passwd='iX2yPaDJYjPAQn', db='podcast', port=3306, charset='utf8')
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute('select rssUrl from rss where feedTitle REGEXP %s', title)
    rssUrl = cursor.fetchone()
    print(rssUrl)
    cursor.execute('select rss2, con from con where rss1 = %s', rssUrl['rssUrl'])
    result = cursor.fetchall()
    data = []
    if not result:
        print('no result')
        
    else:
        for item in result:
            format = {'rss': '', 'con': 1}
            format['rss'] = item['rss2']
            format['con'] = item['con']
            data.append(format)
    cursor.execute('select rss1, con from con where rss2 = %s',
                   rssUrl['rssUrl'])
    result2 = cursor.fetchall()
    print(result2)
    if not result2:
        print('no resutlt2')
    else:
        for item in result2:
            format = {'rss': '', 'con': 1}
            format['rss'] = item['rss1']
            format['con'] = item['con']
            data.append(format)
    dataSend = []
    for i in range(0, len(data)):
        format = {'feedTitle': '', 'feedLink': '', 'img': '', 'con': 1, 'rssUrl': ''}
        cursor.execute('select * from rss where rssUrl = %s', data[i]['rss'])
        result3 = cursor.fetchone()
        print('final')
        if not result3:
            print('no result3')
        else:
            format['feedTitle'] = result3['feedTitle']
            format['feedLink'] = result3['feedLink']
            format['img'] = result3['img']
            format['rssUrl'] = result3['rssUrl']
            format['con'] = data[i]['con']
            dataSend.append(format)
    dataSend = sorted(dataSend, key=lambda k: k['con'], reverse=True)
    print(dataSend)
    return jsonify({'code': 0, 'msg': 'ok', 'data': dataSend})


@app.route('/search/hot', methods=['GET'])
def hotList():
    title = request.args.get('title')
    print(title)
    connection = pymysql.connect(host='localhost', user='root',
                                 passwd='iX2yPaDJYjPAQn', db='podcast', port=3306, charset='utf8')
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute('select * from rss order by hot desc')
    result = cursor.fetchall()
    return jsonify({'code': 0, 'msg': 'ok', 'data': result})

@app.route('/action/like')
def like():
    if not request.args.get('rss1'):  # 檢測是否有數據
        return jsonify({'code': 1, 'msg': 'missing par'})
    if not request.args.get('rss2'):
        return jsonify({'code': 1, 'msg': 'missing par'})
    rss1 = request.args.get('rss1')
    rss2 = request.args.get('rss2')
    print(rss1, rss2)
    if rss1 == rss2:
        return jsonify({'code': 1, 'msg': 'same!'})
    connection = pymysql.connect(host='localhost', user='root',
                                 passwd='iX2yPaDJYjPAQn', db='podcast', port=3306, charset='utf8')
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute('select * from con where rss1 = "'+ rss1 +'" and rss2 = "' + rss2 + '"')
    result = cursor.fetchone()
    if not result:
        cursor.execute('select * from con where rss1 = "'+ rss2+'" and rss2 = "' + rss1 + '"')
        result2 = cursor.fetchone()
        if not result2:
            cursor.execute('insert into con (rss1, rss2) values (%s, %s)', (rss1, rss2))
            cursor.close()
            connection.commit()
            connection.close()
            return jsonify({'code': 0, 'msg': 'ok but'})
        else:
            cursor.execute('update con set con = con + 1 where id = %s', result2['id'])
            cursor.close()
            connection.commit()
            connection.close()
            return jsonify({'code': 0, 'msg': 'ok'})
    else:
        cursor.execute('update con set con = con + 1 where id = %s', result['id'])
        cursor.close()
        connection.commit()
        connection.close()
        return jsonify({'code': 0, 'msg': 'ok'})
    # cursor.execute('select * from con where rss1 = %s', rss1)
    # result = cursor.fetchone()
    # # dataMany = cursor.fetchmany(3)
    # if not result:
    #     cursor.execute('select * from con where rss2 = %s', rss1)
    #     result2 = cursor.fetchone()
    #     print(result2)
    #     if not result2:
    #         # sql = "insert into con (rss1, rss2) values (%s, %s)"
    #         # val = (rss1, rss2)
    #         print('not 2')
    #         cursor.execute('insert into con (rss1, rss2) values (%s, %s)', (rss1, rss2))
    #         # cursor.execute(sql, val)
    #         cursor.close()
    #         connection.commit()
    #         connection.close()
    #         return jsonify({'code': 0, 'msg': 'ok but no record'})
    #     else:
    #         if result2['rss1'] == rss2:
    #             cursor.execute('update con set con = con + 1 where id = %s', result2['id'])
    #             cursor.close()
    #             connection.commit()
    #             connection.close()
    #             return jsonify({'code': 0, 'msg': 'ok'})
    #         else:
    #             cursor.execute('insert into con (rss1, rss2) values (%s, %s)', (rss1, rss2))
    #             # cursor.execute(sql, val)
    #             cursor.close()
    #             connection.commit()
    #             connection.close()
    #             return jsonify({'code': 0, 'msg': 'ok but no record'})
    # else:
    #     if result['rss2'] == rss2:
    #         cursor.execute('update con set con = con + 1 where id = %s', result['id'])
    #         cursor.close()
    #         connection.commit()
    #         connection.close()
    #         return jsonify({'code': 0, 'msg': 'ok'})
    #     else:
    #         print(result['rss2'], rss2)
    #         cursor.execute('insert into con (rss1, rss2) values (%s, %s)', (rss1, rss2))
    #         cursor.close()
    #         connection.commit()
    #         connection.close()
    #         return jsonify({'code': 0, 'msg': 'ok but no record'})

@app.route('/forecast', methods=['GET'])
def forecast():
    if not request.args.get('rss'):  # 檢測是否有數據
        return jsonify({'code': 1, 'msg': 'missing par'})
    rssUrl = {'rssUrl': request.args.get('rss')}
    connection = pymysql.connect(host='localhost', user='root',
                                 passwd='iX2yPaDJYjPAQn', db='podcast', port=3306, charset='utf8')
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute('select date from episode where rssUrl = %s', rssUrl['rssUrl'])
    date = cursor.fetchall()
    # print(date)
    dateList = []
    for item in date:
        # print(item['date'])
        dt = parser.parse(str(item['date']))
        dateList.append(dt)
    dateList.sort(reverse=True)
    listRange = 10
    averge = datetime(2011, 1, 7) - datetime(2011, 1, 7)
    if listRange > len(dateList):
        listRange = len(dateList)
    for i in range(1, listRange):
        averge += dateList[i-1] - dateList[i]
    averge = averge / (listRange - 1)
    sub = datetime.now(timezone.utc) - dateList[0]
    result = (averge - sub).days
    print(averge, sub, result)
    if result < 0:
        result = (datetime(2011, 1, 7) - datetime(2011, 1, 7)).days
        msg = 'It will be released soon'
    else:
        msg = 'It will be released in ' + str(result) + ' days'
    return jsonify({'code': 0, 'msg': msg})
if __name__ == '__main__':
    app.run()
