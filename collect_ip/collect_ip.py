# -*- coding: UTF-8 -*-
import os
from ip_mysql import IpMysql
from pyquery import PyQuery as pq
import lrequest
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


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


def dealresponse(res):
    html = res.content
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
        # if sql.totalofdisabelip() >= 1:
        #     # 存在失效 ip
        #     sql.updatedisableip(data)
        #     pass
        # else:
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
    sql.insert("DELETE from  pi_pool where state = 1")

    if sql.totalip() >= 1000:
        exit('ip 已经更新到 1000 有效')

    while os.path.exists(pid_file) and (current_pid == getpidfromfile(pid_file)):
        lrequest.request(url.format(index), callback=dealresponse, headers={"host": "www.xicidaili.com"})

        index += 1
        if index >= 1800:
            break
    pass

