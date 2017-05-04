# -*- coding: utf-8 -*-

import requests
import cookielib
from pyquery import PyQuery as pq
import sys

reload(sys)
import threading

sys.setdefaultencoding("utf-8")

category = {
    # "news_tech": 0,
    # "news_entertainment": 0,
    # "news_sports": 0,
    # "news_sports": 0,
    "news_hot": 0,
    # "news_society": 0,
    # "news_society": 0,
    # "news_car": 0
}

apiurl = "http://www.toutiao.com/api/pc/feed/?category={0}&utm_source=toutiao&widen=1&max_behot_time={1}&max_behot_time_tmp=0&tadrequire=false&as=A175990077EECF2&cp=59078EBCCFF2DE1"


def ttrequsts(url, **args):
    agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    header = {
        "HOST": "www.toutiao.com",
        "Referfer": "www.toutiao.com",
        "User-Agent": agent
    }
    session = requests.Session()
    session.cookies = cookielib.LWPCookieJar(filename="cookies2.txt")
    try:
        session.cookies.load(ignore_discard=True)
    except:
        print u"failed load cookie"
    try:
        response = session.get(url, headers=header, timeout=10, **args)
        session.cookies.save()
    except Exception as e:
        print e
        return None
    # print response.status_code
    if response and response.status_code == 200:
        return response


def start():
    global category
    # url = apiurl.format(str(int(time.time()))[:10])
    while 1:
        ckey = getTkey()
        url = apiurl.format(ckey, category[ckey])

        print "{0}==={1}".format(ckey, url)
        response = ttrequsts(url)
        # session.cookies.save()
        if response is not None:
            arclist = parselist(response)
            if len(arclist) > 0:
                crawlarc(arclist)


def parselist(response):
    json = response.json()
    print 'next>>>>>>>>>>>{0}'.format(json["next"]["max_behot_time"])
    global category
    ckey = getTkey()
    category[ckey] = json["next"]["max_behot_time"]
    arclist = [item for item in json["data"] if item["article_genre"] == "article" and item["source"] != u"头条问答"]
    return arclist


def crawlarc(alist):
    for data in alist:
        item = {}
        print data["title"]
        print data["source_url"]
        import urlparse
        arcurl = urlparse.urljoin("http://www.toutiao.com", data["source_url"])
        arcres = ttrequsts(arcurl)
        if arcres is not None:
            item["title"] = data["title"]
            item["url"] = arcurl
            # parseArc(arcres, item)
            css = pq(arcres.text).make_links_absolute(arcres.url)
            item["content"] = css.find(".article-content").html()
            item["category"] = getTkey()
            save(item)
        else:
            continue
            # start()


def save(data):
    print "\n{0}--thread is working>>>>>>>>>>>>>>>>>>>>>\n".format(threading.currentThread().getName())
    try:
        import json
        # css = pq(response.text).make_links_absolute(response.url)
        # data["content"] = css.find(".article-content").html()
        res = requests.post("http://192.168.10.254:5678/index.php/xsapi/ucsave", data={"data": json.dumps(data)})
        print res.text
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



