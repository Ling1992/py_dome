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
import json
import sys
reload(sys)
sys.setdefaultencoding("utf8")


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


if __name__ == '__main__':
    # "media_url": "/c/user/5739097906/",
    url = "/c/user//"
    reg = re.compile(r'[0-9]+')
    m = reg.search(url)

    # if m:
    print m.group()
    # else:
    #     print 'not search'
    pass

