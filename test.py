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
import lrequest
import warnings
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
base_url = "http://www.toutiao.com/group/6456945339805991438/"


if __name__ == '__main__':
    lrequest.request('http://www.toutiao.com')
    pass

