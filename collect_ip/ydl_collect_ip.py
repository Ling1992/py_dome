# -*- coding: UTF-8 -*-
import cookielib
import os
import random
import requests
import time

from base_class import func
from ip_mysql import IpMysql
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


def iprequest(request_url, tries=3):
    header = {'User-Agent': random.choice(agent)}
    session = requests.Session()
    session.keep_alive = False
    session.cookies = cookielib.LWPCookieJar(filename="./{}_cookies.txt".format(u'collect_ip'))
    if tries <= 0:
        return None
    response = None
    time.sleep(10)
    try:
        # ignore_discard=True 忽略关闭浏览器丢失 , ignore_expires=True ,忽略失效  --load() 在文件中读取cookie
        session.cookies.load(ignore_discard=True)
    except Exception, e:
        print u"failed load cookie !! Exception:{}".format(e.message)
    try:
        response = session.get(request_url, headers=header, timeout=10)
        time.sleep(random.randint(10, 20))
        session.cookies.save()
        if response.status_code == 200:
            return response
        else:
            print response.status_code, response.reason
            iprequest(request_url, tries - 1)
    except Exception as e:
        print e.message
        iprequest(request_url, tries-1)
        pass
    return response


def save(data):
    # # 2 是否 ip 数是否 大于等于1000
    #     # 大于 等于 只需要更新
    #     if:
    #     else:  # 否则 添加
    if sql.totalip() >= 2000:
        # 只需要更新 失效的 ip
        # if sql.totalofdisabelip() >= 1:
        #     # 存在失效 ip
        #     sql.updatedisableip(data)
        #     pass
        # else:
        if current_pid == getpidfromfile(pid_file):
            if os.path.exists(pid_file):
                os.remove(pid_file)
        # time.sleep(5)
        # exit('ip 已经更新到 1000 有效')
    else:
        # 只做 新增
        print data
        sql.save(data)
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
    category = [
        {"type": "xici", "url": "http://www.xicidaili.com/nn/{}", "end_index": 1800},
        {"type": "ydl", "url": "http://www.ip3366.net/?stype=1&page={}", "end_index": 7},
        {"type": "kdl", "url": "http://www.kuaidaili.com/free/inha/{}/", "end_index": 1800},
    ]

    for a in category:
        index = 1
        category_type = a.get('type')

        while (a.get('end_index')+1 != index) and os.path.exists(pid_file) and (current_pid == getpidfromfile(pid_file)):
            res = iprequest(a.get('url').format(index))
            if res:
                if category_type == "xici":
                    func.xcdl_collect_ip(res.content, callback=save)
                elif category_type == "ydl":
                    func.ydl_collect_ip(res.content, callback=save)
                elif category_type == "kdl":
                    func.kdl_collect_ip(res.content, callback=save)
                else:
                    pass
            else:
                break
            index += 1

    if current_pid == getpidfromfile(pid_file):
        if os.path.exists(pid_file):
            os.remove(pid_file)
