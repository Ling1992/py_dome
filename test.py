# _*_ encoding=utf-8 _*_
import threading
from time import ctime, sleep
import time
import requests
import cookielib
import re
import time
import random
import json
import demjson
from pyquery import PyQuery as pq
from base_class.ling_mysql import MysqlLing
from base_class.ling_request import LingRequest
from collect_ip.ip_mysql import IpMysql
from base_class.base_mysql import MysqlBase
from base_class import func
import json
import os
import HTMLParser
import sys
reload(sys)
sys.setdefaultencoding("utf8")
from base_class.config import Config


def loop(loops, **kwargs):
    print 'sec:', kwargs['index']
    print 'loops : ', loops, 'sec:', ctime(), 'kwargs:', json.dumps("", ensure_ascii=False, encoding='utf-8')
    sleep(kwargs['index'])
    print 'loops : ', loops, 'sec:', ctime(), 'current thread name:', threading.current_thread().name
    test(loops, kwargs)
    log(kwargs)


def test(loops, arg):
    print __name__, arg
    log(arg)
    print 'current thread name:', threading.current_thread().name


def log(content, key_str='default'):
    with open('cache/{}_at_{}.log'.format(threading.current_thread().name, time.strftime("%Y-%m-%d", time.localtime(time.time()))), 'a') as f:
        f.write('{} -->>'.format(key_str))
        f.write('{}:\n'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))))
        f.write('\t')
        f.write(repr(content))
        f.write('\n')


def start():
    print threading.currentThread().name
    request = LingRequest()
    res = request.request("http://www.toutiao.com/group/6460022476294570253/")
    print res.status_code, res.reason
    time.sleep(2)
    pass


cookies_path = "test_cookies.txt"
base_url = "http://www.toutiao.com/group/6440948651246289154/"


if __name__ == '__main__':
    # with open(cookies_path, 'w') as f:
    #     f.write("")
    # session = requests.session()
    # session.keep_alive = False
    # session.cookies = cookielib.LWPCookieJar(filename=cookies_path)
    # header = {
    #     "Host": "www.toutiao.com",
    #     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    # }
    # session.get("http://www.toutiao.com/", headers=header, timeout=10)
    # session.cookies.save()
    #
    proxies = {'https': 'https://111.165.209.49:53281'}

    session = requests.session()
    session.keep_alive = False
    session.cookies = cookielib.LWPCookieJar(filename=cookies_path)

    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    }

    try:
        session.cookies.load(ignore_discard=True)
    except Exception as e:
        print u"session.cookies.load error : ", e.message

    respond = session.get(base_url, timeout=5, proxies=proxies)

    print respond.status_code, respond.reason

    with open('test.html', 'w') as f:
        f.write(respond.content)

    # content = None
    # with open('test.html', 'r') as f:
    #     content = f.read()
    # article = func.get_article_one(content, 'articleInfo', 'content')
    # # print article
    # sql = MysqlBase({'db': 'ling_test'})
    #
    # sql.insert("insert into test(text) VALUES ('%s')" % article)

