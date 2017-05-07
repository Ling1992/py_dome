# -*- coding: utf-8 -*-

import requests
import cookielib
import json
import Queue
from pyquery import PyQuery as pq
import sys

reload(sys)
import threading

sys.setdefaultencoding("utf-8")

saver = 1

category = {
    "news_tech": 0,
    "news_entertainment": 0,
    "news_sports": 0,
    "news_sports": 0,
    "news_hot": 0,
    "news_society": 0,
    "news_society": 0,
    "news_car": 0
}

q = Queue.Queue(128)

apiurl = "http://www.toutiao.com/api/pc/feed/?category={0}&utm_source=toutiao&widen=1&max_behot_time={1}&max_behot_time_tmp=0&tadrequire=false&as=A175990077EECF2&cp=59078EBCCFF2DE1"


def ttrequsts(url, **args):
    agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    header = {
        # "HOST": "www.toutiao.com",
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
        import urlparse
        arcurl = urlparse.urljoin("http://www.toutiao.com", data["source_url"])
        arcres = ttrequsts(arcurl)
        if arcres is not None:
            item["title"] = data["title"]
            item["url"] = arcurl
            # parseArc(arcres, item)
            css = pq(arcres.text).make_links_absolute(arcres.url)
            item["content"] = css.find(".article-content").html()
            item["category"] = category[getTkey()]
            # print data["title"]
            # print data["source_url"]
            if item["content"] is None:
                item["content"] = zwen(arcurl)
                with open("nocontent.log", "a") as f:
                    f.write(item["url"])
                    return
                if item["content"] is None:
                    with open("nocontent.log", "a") as f:
                        f.write(item["url"])
                        return
            q.put(item)
            # save(item)
        else:
            continue
            # start()


def zwen(url):
    return None


class M():
    def __init__(self, name):
        self.name = getattr(self, name)

    def __call__(self):
        while 1:
            self.name()

    def local(self):
        print q.qsize()
        data = q.get()
        print data["title"]

    def remote(self):
        data = q.get()
        print "\n>>>>>>>>>>>>>>>>>>>qsize{0}".format(q.qsize())
        print "\n{0}--thread is working>>>>>>>>>>>>>>>>>>>>>\n".format(threading.currentThread().getName())
        try:
            import json
            # css = pq(response.text).make_links_absolute(response.url)
            # data["content"] = css.find(".article-content").html()
            res = requests.post("http://192.168.10.254:5678/index.php/xsapi/ucsave", data={"data": json.dumps(data)})
            jsondata = res.json()
            print jsondata
            if jsondata["code"] == 2:
                with open("mysql2.log", "a") as f1:
                    f1.write(jsondata["msg"])

        except Exception as e:
            with open("mysql.log", "a") as f:
                f.write(e.message)
            print e
            pass


def savetxt():
    while 1:
        data = q.get()
        # print data["title"]
        print q.qsize()


def getTkey():
    ckey = threading.currentThread().getName()
    return ckey


def main():
    skey = "local"

    if len(sys.argv) > 1:
        skey = sys.argv[1]
    # savetool = getattr(m, skey)
    m = M(skey)
    threads = []
    for _, v in category.iteritems():
        tf = threading.Thread(target=start, name=_)
        threads.append(tf)
    for i in xrange(saver):
        ts = threading.Thread(target=m, name="save{0}".format(i))
        threads.append(ts)
    # tsave = threading.Thread(target=savetxt, name="i an save")

    for t in threads:
        t.start()
    # tsave.start()
    for t in threads:
        t.join()
        # tsave.join()


if __name__ == "__main__":
    main()

