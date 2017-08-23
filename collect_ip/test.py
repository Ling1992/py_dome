# -*- coding: UTF-8 -*-
from pyquery import PyQuery as pq
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

if __name__ == u'__main__':
    print 'run'

    html = None
    with open('./test.html', 'r') as f:
        html = f.read()
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
                        data['type'] = td.html()
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
                    print data
                    print '-' * 88
        pass

    pass

