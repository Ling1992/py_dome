# -*- coding: UTF-8 -*-
from pyquery import PyQuery as pq
from ip_mysql import IpMysql
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
    sql = IpMysql({'db': 'python_bases'})
    # # 设置 state 为 0
    sql.disableip('113.133.86.172')
    # # 随机 获取 state 为 1 的 ip

    data = sql.getrandomip()
    print data['type']
    print '{}://{}:{}'.format(data['type'], data['ip'], data['port'])
    print sql.haveip('113.133.86.1721')
    if sql.haveip('113.133.86.1721') is False:
        print 'yes'
    else:
        print 'no'
    pass

