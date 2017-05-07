# _*_ encoding=utf-8 _*_
import threading
from time import ctime, sleep
import time
import requests
import re
import time
import random


def loop(loops, **kwargs):
    print 'sec:', kwargs['index']
    print 'loops : ', loops, 'sec:', ctime(), 'kwargs:', repr(kwargs)
    sleep(kwargs['index'])
    print 'loops : ', loops, 'sec:', ctime(), 'current thread name:', threading.current_thread().name
    test(loops, kwargs)
    log(kwargs)
    # 抓取代理IP
    ip_totle = []  # 所有页面的内容列表
    for page in range(2, 6):
        url = 'http://ip84.com/dlgn/' + str(page)
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64)"}
        response = requests.get(url, headers=headers)
        content = response.content
        print('get page', page)
        pattern = re.compile('<td>(\d.*?)</td>')  # 截取<td>与</td>之间第一个数为数字的内容
        ip_page = re.findall(pattern, str(content))
        ip_totle.extend(ip_page)
        time.sleep(random.choice(range(1, 3)))
    # 打印抓取内容
    print('代理IP地址     ', '\t', '端口', '\t', '速度', '\t', '验证时间')
    for i in range(0, len(ip_totle), 4):
        print(ip_totle[i], '    ', '\t', ip_totle[i + 1], '\t', ip_totle[i + 2], '\t', ip_totle[i + 3])



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
    category = {'new': {'name': '新闻', 'index': 2}, 'sport': {'name': '运动', 'index': 8}}

    threads = []

    for key in category:
        print key, category[key]['index'], category[key]['name']
        t = threading.Thread(target=loop, kwargs={'loops': key, 'index': category[key]['index'], 'name': category[key]['name']}, name='{}121'.format(key))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

