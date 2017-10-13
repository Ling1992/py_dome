# -*- coding: utf-8 -*-
import requests
import cookielib
import time
from . import l_mysql
from base_class import func


class LRequest(object):
    sql = None
    agent = None
    host = None
    proxies = None
    ip_data = None
    index = 1
    cookie_path = './l_request.cookies'

    def __init__(self):
        # # mysql
        try:
            self.sql = l_mysql.LMysql({'db': 'python_bases'})
        except Exception, e:
            print 'ip mysql 连接失败'
            print e.message
            self.sql = None
        self.update_arg()
        pass

    def request(self, url, retries, callback, **kwargs):

        if self.index >= 15:  # request 循环 15 次 退出 request
            return None

        headers = kwargs.get("headers")
        if headers is None:
            headers = {}
        headers['User-Agent'] = self.agent
        kwargs["headers"] = headers
        if self.sql is not None:
            kwargs["proxies"] = self.proxies
        proxies = kwargs.get("proxies")

        self.index += 1

        session = requests.session()
        session.keep_alive = False
        session.cookies = cookielib.LWPCookieJar(filename=self.cookie_path)

        try:
            session.cookies.load(ignore_discard=True)
        except Exception as e:
            print u"session.cookies.load error : ", e.message

        try:
            print url, proxies
            respond = session.get(url, timeout=6, **kwargs)
            session.cookies.save()
            if respond and respond.status_code == 200:  # 请求成功
                time.sleep(5)  # 请求 间隔
                if callback:
                    callback(respond)
                print "get respond :", url
            elif respond.status_code == 407:  # # 请求失败 需要代理认证
                print 'proxy error :', respond.status_code
                self.sql.disable_ip(self.ip_data['ip'])
                self.update_arg(1)  # 只需要 更改 代理 ip
                return self.request(url, retries, callback, **kwargs)
            elif respond.status_code == 404:
                return None
            elif respond.status_code == 403 or respond.status_code == 502 or respond.status_code == 503:    # # 主要是 403 502 代理被封
                print 'error:'
                print respond.status_code, respond.reason, url
                time.sleep((5 - retries) * 5)
                self.update_arg()
                if respond.status_code == 502:
                    headers['host'] = None   # # 头条 会出现该问题
                    kwargs.setdefault("headers", headers)
                return self.request(url, retries, callback, **kwargs)
            else:   # # 未知 错误 出现
                print '未知错误 error:'
                print respond.status_code, respond.reason, url
                time.sleep((5 - retries) * 5)
                self.update_arg()
                return self.request(url, retries-1, callback, **kwargs)
        except Exception as e:
            if func.check_ip_exception(e):  # # 代理 拒绝 或 连接 超时
                print 'proxy error \n', e.message
                # self.sql.disable_ip(self.ip_data['ip'])
                self.update_arg(1)
                time.sleep(3)
                return self.request(url, retries, callback, **kwargs)
            elif "Connection aborted" in e.message:
                self.clear_cookies()
                self.update_arg(0)
                return self.request(url, retries-1, callback, **kwargs)
                pass
            else:
                print u"无法连接网络 ！！！", e.message
                self.update_arg()
                time.sleep(5)
                if retries <= 1:
                    exit('无法连接网络 ！！！')
                return self.request(url, retries - 1, callback, **kwargs)
        self.index = 1
        return respond

    def update_arg(self, update_type=0):
        if update_type == 0:
            self.agent = func.get_random_agent()
            if self.sql is not None:
                self.ip_data = self.sql.get_random_ip()
                self.proxies = {
                    self.ip_data['type']: "{}://{}:{}".format(self.ip_data['type'], self.ip_data['ip'],
                                                              self.ip_data['port'])}
        elif update_type == 1:
            if self.sql is not None:
                self.ip_data = self.sql.get_random_ip()
                self.proxies = {
                    self.ip_data['type']: "{}://{}:{}".format(self.ip_data['type'], self.ip_data['ip'],
                                                              self.ip_data['port'])}
        else:
            self.agent = func.get_random_agent()

    def clear_cookies(self):
        with open(self.cookie_path, 'w') as f:
            f.write("")
        pass

    def __exit__(self, *args):
        del self.sql
        pass

    def __enter__(self):
        return self
        pass
