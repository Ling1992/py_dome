# -*- coding: UTF-8 -*-
import cookielib
import os
import random
import requests
import time
from ip_mysql import IpMysql
from pyquery import PyQuery as pq
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

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


def init():
    pwd = os.getcwd()
    print pwd
    os.chdir(pwd)


def getpidfromfile(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as fi:
            pid_str = fi.read()
    else:
        pid_str = 0
    return int(pid_str)


def iprequest(request_url):
    header = {'User-Agent': random.choice(agent)}
    session = requests.Session()
    session.keep_alive = False
    session.cookies = cookielib.LWPCookieJar(filename="./{}_cookies.txt".format(u'collect_ip'))
    response = None
    try:
        # ignore_discard=True 忽略关闭浏览器丢失 , ignore_expires=True ,忽略失效  --load() 在文件中读取cookie
        session.cookies.load(ignore_discard=True)
    except Exception, e:
        print u"failed load cookie !! Exception:{}".format(e.message)
    try:
        response = session.get(request_url, headers=header, timeout=61)
        time.sleep(random.randint(10, 20))
        session.cookies.save()
        if response.status_code == 200:
            return response
        else:
            print response.status_code, response.reason
    except Exception as e:
        print e.message
        pass
    return response


def dealresponse(html):
    if html:
        dom = pq(html)
        trs = dom('table')('tr')
        i = 0
        for tr in trs.items():
            i += 1
            if i == 1:
                continue
            else:
                tds = tr('td')
                data = {}
                j = 0
                for td in tds.items():
                    j += 1
                    if j == 2:
                        data['ip'] = td.html()
                    if j == 3:
                        data['port'] = td.html()
                    if j == 6:
                        if td.html() == u'HTTP':
                            data['type'] = 1
                        else:
                            data['type'] = 2
                    if j == 7:
                        race = strtosecond(td('div').attr('title'))
                        if race > 5:
                            data = {}
                            continue
                    if j == 8:
                        connect_time = strtosecond(td('div').attr('title'))
                        if connect_time > 5:
                            data = {}
                            continue
                    if j == 9:
                        effective_time = strtosecond(td.html())
                        if effective_time <= 120:
                            data = {}
                            continue
                if data:
                    save(data)
                    # print data
                    # print '-' * 88
        pass


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


def save(data):
    # # 2 是否 ip 数是否 大于等于1000
    #     # 大于 等于 只需要更新
    #     if:
    #     else:  # 否则 添加
    if sql.totalip() >= 1000:
        # 只需要更新 失效的 ip
        if sql.totalofdisabelip() >= 1:
            # 存在失效 ip
            sql.updatedisableip(data)
            pass
        else:
            exit('ip 已经更新到 1000 有效')
    else:
        # 只做 新增
        sql.save(data)
        pass
    pass


if __name__ == u'__main__':
    print u'run'
    init()
    sql = IpMysql({'db': 'python_bases'})
    current_pid = os.getpid()
    # # 处理 pid
    pid_file = u'./collect_ip.pid'
    if os.path.exists(pid_file):
        print u'pid 文件存在 ！！！'
        if current_pid == getpidfromfile(pid_file):
            print u'系统错误 :  当前pid 等于 file pid'
            exit()
            pass
        else:
            with open(pid_file, 'w') as f:
                f.write(str(current_pid))
    else:
        with open(pid_file, 'w') as f:
            f.write(str(current_pid))

    # # 1 判断 ip 是否存在 并且是有效的
    # # 处理逻辑
    url = "http://www.xicidaili.com/nn/{}"
    index = 1
    while os.path.exists(pid_file) and (current_pid == getpidfromfile(pid_file)):
        res = iprequest(url.format(index))
        if res:
            dealresponse(res.content)
            pass
        index += 1
        if index >= 1800:
            break
    pass

