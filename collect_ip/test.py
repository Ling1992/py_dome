# -*- coding: UTF-8 -*-
from pyquery import PyQuery as pq
from ip_mysql import IpMysql
import random
import requests
import cookielib
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def strtosecond(time_str):
    if time_str:
        if '秒' in time_str:
            return strtoint(time_str)
        elif '分' in time_str or '分钟' in time_str:
            return strtoint(time_str) * 60
        elif '小时' in time_str:
            return strtoint(time_str) * 60 * 60
        else:
            return 10000
    else:
        return 0


def strtoint(time_str):
    time_str = time_str.replace('秒', '')
    time_str = time_str.replace('分钟', '')
    time_str = time_str.replace('分', '')
    time_str = time_str.replace('小时', '')
    return eval(time_str)


def test():
    print category_type


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

request_url = "http://www.kuaidaili.com"
if __name__ == u'__main__':

    # header = {'User-Agent': random.choice(agent)}
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        # 'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'www.kuaidaili.com',
        # 'Referer': 'http://www.cnvd.org.cn/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': random.choice(agent),
        # 'Cookie': 'yd_cookie=f880ee0e-234b-4dc1ef5bda9b069984f1951f5544ecfc0f85; _ydclearance=113434f7d2690255ba4a7991-d126-44ee-a715-314e6b37ee9d-1505293081; channelid=0; sid=1505287882234940; Hm_lvt_7ed65b1cc4b810e9fd37959c9bb51b31=1505266242,1505268488,1505269401; Hm_lpvt_7ed65b1cc4b810e9fd37959c9bb51b31=1505288426; _ga=GA1.2.892942617.1505266242; _gid=GA1.2.758269675.1505266242'

    }
    session = requests.Session()
    session.keep_alive = False
    session.cookies = cookielib.LWPCookieJar(filename="./test_cookies.txt")

    try:
        # ignore_discard=True 忽略关闭浏览器丢失 , ignore_expires=True ,忽略失效  --load() 在文件中读取cookie
        session.cookies.load(ignore_discard=True)
    except Exception, e:
        print u"failed load cookie !! Exception:{}".format(e.message)

    try:
        response = session.get(request_url, headers=headers, timeout=10)
        session.cookies.save()
        print response.status_code, response.reason
        print response.content
        if response.status_code == 200:
            with open('test.html', 'w') as f:
                f.write(response.content)

    except Exception as e:
        print e.message
        pass

    # res = requests.get(request_url)
    # with open('test.html', 'w') as f:
    #     f.write(res.content)
        # html = f.read()
    # dom = pq(html)
    # trs = dom('tbody')('tr')
    #
    # for tr in trs.items():
    #     tds =tr('td')
    #     j = 0
    #     for td in tds.items():
    #         if j == 0:
    #             print td.html()
    #         elif j == 1:
    #             print td.text()
    #         elif j == 3:
    #             print td.text()
    #         elif j == 6:
    #             print td.text()
    #         j += 1

    # pass

