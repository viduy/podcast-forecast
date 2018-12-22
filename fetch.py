import feedparser
import pymysql

def catchFeed(url):
    # rss_url = 'https://s.anw.red/rss.xml'
    rss_url = str(url)
    # rss_url = "https://getpodcast.xyz/cgi/parse?url=" + rss_url
    # 获得订阅
    feeds = feedparser.parse(rss_url)
    connection = pymysql.connect(host='localhost',user='root',passwd='iX2yPaDJYjPAQn',db='podcast',port=3306,charset='utf8') 
    cursor = connection.cursor()
    # 获得rss版本
    print(feeds.version)
    # 获得Http头
    print(feeds.headers)
    
    print(feeds.headers.get('content-type'))
    # rss的标题
    print(feeds['feed']['title'])
    # 链接

    print(feeds['feed']['link'])

    rssData = [rss_url, feeds['feed']['title'], feeds['feed']['link']]
    # 子标题
    # print(feeds.feed.subtitle)
    # 查看文章数量
    try:
        cursor.execute('insert into rss values (%s,%s,%s)', rssData)
    except:
        print("Error: insert failed")
    else:
        print("YES!!!")
    # cursor.execute('insert into rss values (%s,%s,%s)', rssData)
    print(len(feeds['entries']))
    # 获得第一篇文章的标题
    for feed in feeds['entries']:
        # print(feed['title'])
        # print(feed['link'])
        # print(feed['image']['href'])
        # print(feed['published'])
        try:
            episode = [rss_url, feed['title'], feed['link'], feed['image']['href'], feed['published']]
            cursor.execute('insert into episode values (%s,%s,%s,%s,%s)', episode)
        except:
            print("Error: insert failed")
        else:
            print("YES!!!")
        
    connection.commit()
    cursor.close()
    connection.close()
        
rssList = [
    "http://rss.lizhi.fm/rss/1569925.xml",
    "https://s.anw.red/rss.xml",
    "https://talk.swift.gg/static/rss.xml",
    "http://rss.lizhi.fm/rss/14275.xml",
    "https://daringfireball.net/thetalkshow/rss",
    "https://thetype.com/feed/typechat/"
]

# for rss in rssList:
#     catchFeed(rss)

catchFeed(rssList[5])


