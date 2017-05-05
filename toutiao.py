# -*- coding: utf-8 -*-

import cookielib
import sys

import requests
from pyquery import PyQuery as pq

from base_class.ling_mysql import MysqlLing

reload(sys)
import threading

sys.setdefaultencoding("utf-8")

category = {
    # "news_tech": 0,
    # "news_entertainment": 0,
    # "news_sports": 0,
    # "news_sports": 0,
    "news_hot": {"time_sec": 0, "for_times": 1},
    # "news_society": 0,
    # "news_society": 0,
    # "news_car": 0
}
model = 1

apiurl = "http://www.toutiao.com/api/pc/feed/?category={0}&utm_source=toutiao&widen=1&max_behot_time={1}&max_behot_time_tmp=0&tadrequire=false&as=A175990077EECF2&cp=59078EBCCFF2DE1"
apiurl1 = "http://www.toutiao.com/api/pc/feed/?category=news_hot&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=false&as=A175990077EECF2&cp=59078EBCCFF2DE1"


def ttrequsts(url, **args):
    print url
    agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    header = {
        # "HOST": "www.toutiao.com", # 解决 301 重定向问题
        "Referfer": "www.toutiao.com",
        "User-Agent": agent
    }
    # 默认的是FileCookieJar没有实现save函数。
    # 而MozillaCookieJar或LWPCookieJar都已经实现了。
    # 所以可以用MozillaCookieJar或LWPCookieJar，去自动实现cookie的save。
    # 实现，通过文件保存cookie。
    # 建议用LWPCookieJar，其保存的cookie，易于人类阅读
    session = requests.Session()
    session.cookies = cookielib.LWPCookieJar(filename="cache/cookies2.txt")
    try:
        # ignore_discard=True 忽略关闭浏览器丢失 , ignore_expires=True ,忽略失效  --load() 在文件中读取cookie
        session.cookies.load(ignore_discard=True)
    except:
        print u"failed load cookie"
    try:
        response = session.get(url, headers=header, timeout=10, **args)
        session.cookies.save()
    except Exception as e:
        print e
        return None
    print response.status_code, response.reason
    if response and response.status_code == 200:
        return response


def start():
    global category
    global model
    # url = apiurl.format(str(int(time.time()))[:10])
    while 1:
        ckey = getTkey()

        # python从2.6开始支持format
        # data = {'first': 'Hodor', 'last': 'Hodor!'}
        # Old
        # '%(first)s %(last)s' % data
        # New
        # '{first} {last}'.format(**data)
        # Output
        # Hodor Hodor!

        url = apiurl.format(ckey, category[ckey])
        # url = apiurl1
        print "{0}==={1}".format(ckey, url)
        response = ttrequsts(url)
        # session.cookies.save()
        if response is not None:
            arclist = parselist(response)
            if len(arclist) > 0:
                crawlarc(arclist)


def parselist(response):
    with open('title_list_content.txt', 'w') as f:
        f.write(response.content)
    json = response.json()
    print 'next>>>>>>>>>>>{0}'.format(json["next"]["max_behot_time"])
    global category
    ckey = getTkey()
    category[ckey] = json["next"]["max_behot_time"]
    print 'list count origin :{}'.format(len(json["data"]))
    arclist = [item for item in json["data"] if item["article_genre"] == "article" and item["source"] != u"头条问答"]
    return arclist


def crawlarc(alist):
    print "list count ---> {}".format(len(alist))
    for data in alist:
        item = {}
        # print data["title"]
        # print data["source_url"]
        import urlparse
        arcurl = urlparse.urljoin("http://www.toutiao.com", data["source_url"])
        arcres = ttrequsts(arcurl)
        if arcres is not None:
            item["title"] = data["title"]
            item["tag"] = data["tag"]
            item["group_id"] = data["group_id"]
            item["behot_time"] = data["behot_time"]
            item["url"] = arcurl
            # parseArc(arcres, item)
            css = pq(arcres.text).make_links_absolute(arcres.url)
            content = css.find(".article-content").html()
            item["category"] = getTkey()

            if not content or not len(content):
                content = css('article').html()
            if not content or not len(content):
                content = css.find(".text").html()
            if not content or not len(content):
                print 'content:{}'.format(repr(content))
                if data["source"] == u"专题":
                    print '专题跳过'
                    continue
                else:
                    raise Exception('content is null !!')

            item['content'] = content
            save(item)

        else:
            print 'article respond is null !!'
            continue


def save(item):
    print "\n{0}--thread is working>>>>>>>>>>>>>>>>>>>>>\n".format(threading.currentThread().getName())
    try:
        # import json
        # css = pq(response.text).make_links_absolute(response.url)
        # data["content"] = css.find(".article-content").html()
        # res = requests.post("http://192.168.10.254:5678/index.php/xsapi/ucsave", data={"data": json.dumps(data)})
        # print res.text
        """
            sql 操作
        """
        ling_con = MysqlLing()
        count = ling_con.count("select * from article_list where group_id='%s'"
                               % item.get('group_id'))
        print count
        if count:
            print '数据 重复！！！'
            res = False
        else:
            print '新增 数据 ！！！'
            res = ling_con.insert(
                "insert into article_list(title, abstract, tag, group_id, original_time) VALUES ('%s', '%s', '%s', '%s', '%s')" % (
                item.get('title'), item.get('abstract'), item.get('tag'), item.get('group_id'), item.get('behot_time')))
            print res
            if res:
                pass
            else:
                raise Exception('insert article_list error ')
            res = ling_con.insert("INSERT INTO article(article_id, title, article) VALUES ('%s', '%s', '%s')" % (
            item.get('group_id'), item.get('title'), item.get('content')))
            print res
            if res:
                print 'insert article success !!'
            else:
                raise Exception('insert article error ')

        print "\n"
    except Exception as e:
        print e
        pass


def getTkey():
    ckey = threading.currentThread().getName()
    return ckey


if __name__ == "__main__":

    threads = []
    for _, v in category.iteritems():
        tf = threading.Thread(target=start, name=_)
        threads.append(tf)

    for t in threads:
        t.start()
    for t in threads:
        t.join()



