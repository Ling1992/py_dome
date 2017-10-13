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
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
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
base_url = "http://www.toutiao.com/group/6467695728256188685/"


if __name__ == '__main__':

    # with open('test.pid', "w") as f:
    #     f.write("")
    #
    # driver = webdriver.Chrome()
    #
    # driver.get("http://www.toutiao.com")

    # time.sleep(10)
    #
    # driver.find_element_by_css_selector(".container > .index-channel > div > .channel > ul > li > a[href='/ch/news_tech/']").click()
    #
    # time.sleep(10)
    #
    # group_id = driver.find_element_by_css_selector(".container > .index-content > div[riot-tag='feedBox'] > div > div > div > ul > li").get_attribute("group_id")
    #

    # time.sleep(2)
    # driver.find_element_by_tag_name("body").send_keys(Keys.COMMAND, "t")

    # driver.get("http://www.toutiao.com/group/"+group_id)

    # time.sleep(10)
    #
    # driver.back()

    # while os.path.exists("test.pid"):
    #     time.sleep(1)
    #     pass
    #
    # driver.quit()

    session = requests.session()
    session.keep_alive = False
    session.cookies = cookielib.LWPCookieJar(filename=cookies_path)

    try:
        session.cookies.load()
    except Exception as e:
        print u"session.cookies.load error : ", e.message

    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
               "host": "www.xicidaili.com"}

    respond = session.get("http://www.xicidaili.com", timeout=20, proxies={"http": "182.92.242.11:80"}, headers=headers)

    session.cookies.save()

    print respond.status_code, respond.reason

    pass

