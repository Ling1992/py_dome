# -*- coding: utf-8 -*-
import requests
import random
import cookielib
import time
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

sys.path.append("../")
from collect_ip.ip_mysql import IpMysql


agent = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"
    ]


class LingRequest(object):

    def __init__(self):
        self.ip_sql = IpMysql({'db': 'python_bases'})
        self.a_u = random.choice(agent)
        if self.ip_sql.totalip() >= 1:
            self.ip_data = self.ip_sql.getrandomip()
        else:
            exit(' mysql 中已经没有 ip 可以 用')
        self.cookies_file_path = u"./cookies.txt"

    def request(self, base_url, retries=3):

        if retries < 0:
            self.__update_request()
            retries = 3

        header = {
            "Host": "www.toutiao.com",
            "User-Agent": self.a_u
        }

        proxies = {self.ip_data['type']: "{}://{}:{}".format(self.ip_data['type'], self.ip_data['ip'], self.ip_data['port'])}

        session = requests.session()

        session.keep_alive = False
        session.cookies = cookielib.LWPCookieJar(filename=self.cookies_file_path)

        try:
            session.cookies.load(ignore_discard=True)
        except Exception as e:
            print e
            print u"session.cookies.load error"
        try:
            respond = session.get(base_url, headers=header, timeout=5, proxies=proxies)
            session.cookies.save()
            if respond and respond.status_code == 200:
                time.sleep(10)
                print "get respond "
            elif respond.status_code == 407:
                print 'proxy error !!', respond.status_code
                self.__update_request()
                return self.request(base_url, retries)
            else:
                print 'error'
                print respond.status_code, respond.reason
                time.sleep((4 - retries) * 8)
                return self.request(base_url, retries-1)
        except Exception as e:
            if self.ip_sql.check_exception(e):
                print 'proxy error!!!!', e.message
                self.__update_request()
                return self.request(base_url, retries)
            else:
                print u"session.cookies.load error"
                print e.message
                time.sleep(5)
                if retries <= 1:
                    exit('无法连接网络 ！！！')
                return self.request(base_url, retries - 1)
        return respond

    def __update_request(self):
        with open(self.cookies_file_path, 'w') as f:
            f.write("")
        self.ip_sql.disableip(self.ip_data.get('ip'))
        self.a_u = random.choice(agent)
        if self.ip_sql.totalip() >= 1:
            self.ip_data = self.ip_sql.getrandomip()
        else:
            exit(' mysql 中已经没有 ip 可以 用')





















