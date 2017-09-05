# -*- coding: utf-8 -*-
import requests
import random
import cookielib
import Queue
import threading
import time
import json
import os
import sys
import re

sys.path.append("../")
from collect_ip.ip_mysql import IpMysql
from base_class.SSDB import SSDB
from base_class.config import Config
from base_class import func

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
category = [
        "news_hot",                 # 热点
        "news_society",             # 社会
        "news_entertainment",       # 娱乐
        "news_tech",                # 科技
        "news_sports",              # 体育
        "news_car",                 # 汽车
        "news_finance",             # 财经
        "funny",                    # 搞笑
        "news_military",            # 军事
        "news_fashion",             # 时尚
        "news_discovery",           # 探索
        "news_regimen",             # 养生
        "news_essay",               # 美文
        "news_history",             # 历史
        "news_world",               # 国际
        "news_travel",              # 旅游
        "news_baby",                # 育儿
        "news_story",               # 故事
        "news_game",                # 游戏
        "news_food"                 # 美食
    ]
api_uri = "http://www.toutiao.com/api/pc/feed/?category={0}&utm_source=toutiao&widen=1&max_behot_time={1}&max_behot_time_tmp=0&tadrequire=false"
reg = re.compile(r'[0-9]+')  # "media_url": "/c/user/5739097906/",


class TTSpider(object):

    config = Config(dir="tt")
    ssdb = SSDB(config.get_item("ssdb", "host"), config.get_int("ssdb", "port"))
    ip_sql = IpMysql({'db': config.get_item("mysql_base", "db")})
    ip_in_q = Queue.Queue(128)
    ip_out_q = Queue.Queue(128)
    ip_data = None
    a_u = None
    pid_file_path = u""
    project_path = u""
    pid = str(os.getpid())
    data_save_q = Queue.Queue(256)
    request_index = {}  # #     request 循环 次数  超出 n 次退出 request

    # 初始化
    def __init__(self):
        self.project_path = os.path.dirname(os.path.realpath(__file__))
        self.pid_file_path = self.project_path + "/" + self.__class__.__name__ + ".pid"
        self.create_pid_file()

    # pid  处理
    def create_pid_file(self):
        if not os.path.exists(self.pid_file_path):
            with open(self.pid_file_path, 'w') as f:
                f.write(self.pid)
            pass
        else:
            print u".pid 已经存在 ！！ 请及时处理！！"
            os.remove(self.pid_file_path)
            with open(self.pid_file_path, 'w') as f:
                f.write(self.pid)
            time.sleep(10)  # # 10秒 等待任务结束

    def del_pid_file(self):
        if self.pid == self.get_pid_str():
            if os.path.exists(self.pid_file_path):
                os.remove(self.pid_file_path)

    def get_pid_str(self):
        if os.path.exists(self.pid_file_path):
            with open(self.pid_file_path, 'r') as f:
                pid_str = f.read()
        else:
            pid_str = 0
        return pid_str

    def run(self):

        print u'run'
        th = []

        t = threading.Thread(target=TTSpider.ip_in_work, args=(self,), name='ip_in_queue')
        th.append(t)

        for t in category:
            self.request_index[t] = 0
            tf = threading.Thread(target=TTSpider.work, args=(self,), name=t)
            th.append(tf)
        t = threading.Thread(target=TTSpider.ip_out_work, args=(self,), name='ip_out_queue')
        th.append(t)
        t = threading.Thread(target=TTSpider.data_save_work, args=(self,), name='data_queue')
        th.append(t)

        for t in th:
            t.start()
        for t in th:
            t.join()

        print 'game over'
        if os.path.isfile(self.pid_file_path):
            self.del_pid_file()

    def work(self):
        print 'work!!!'
        name = threading.currentThread().name
        behot_time = 0
        work_index = 3
        self.__update_request()
        while os.path.exists(self.pid_file_path) and self.pid == self.get_pid_str() and work_index:
            print 'work'
            work_index -= 1

            response = self.request(api_uri.format(name, behot_time))

            try:
                json_res = response.json()
            except Exception, e:
                print "response.json() ->> error "
                print "error : ", e.message, "url:", api_uri.format(name, behot_time)
                print "response content :", response
                continue

            try:
                arclist = [item for item in json_res["data"]
                           if (item["article_genre"] == "article" or item["article_genre"] == "gallery")
                           and item["source"] != u"头条问答" and item["source"] != u"专题"]
                print arclist
            except Exception, e:
                print u"article list 处理出现错误 ！！", e.message
                print u"article list: ", json_res['data']
                continue

            # 文章获取
            if arclist and len(arclist) >= 1:
                for data in arclist:
                    self.get_article(data)

        print 'work over'

    def get_article(self, data):
        item = {}

        if data.get("source_url"):
            pass
        else:
            print u'error: source_url not find'
            print data
            return None

        res = self.ssdb.request('get', [data['source_url']])
        if res.code == 'ok':
            return None
        else:
            pass

        arcurl = "http://www.toutiao.com{}".format(data["source_url"])
        response = self.request(arcurl)

        if response is not None:
            title, number = re.subn("'", "\\'", str(data.get("title")))  # 解决 单引号 插入数据库 出错问题
            data['title'] = title

            content = func.get_article(response, data)

            if content:
                # toutiao_article_category 分类 数据源
                item["category_word"] = data.get("tag")
                item["category_name"] = data.get('chinese_tag')
                # toutiao_article_0x 文章 数据源
                content, number = re.subn("\r", "\n", str(content))  # 解决 \r 插入数据库 值为空的问题
                content, number = re.subn("'", "\\'", str(content))  # 解决 单引号 插入数据库 出错问题
                item['article_content'] = content
                # toutiao_article_list 列表 数据源
                item["title"] = title
                item['abstract'] = data.get('abstract')
                item['image_url'] = data.get('image_url')
                item["create_date"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data.get("behot_time")))
                item["url"] = response.url  # 文章url 重定向后 url //唯一性判断
                item["source_url"] = data["source_url"]
                item["group_id"] = data.get('group_id')
                # toutiao_author 作者 数据源
                if data.get('media_url'):
                    m = reg.search(data.get('media_url'))
                    if m:
                        item['author_id'] = m.group()
                    else:
                        item['author_id'] = 0
                else:
                    item['author_id'] = 0
                name = threading.currentThread().name
                print name
                if name == "news_hot":
                    item['is_hot'] = 1
                print('push save queue!!')
                # 放入队列
                print(u"put queue start")
                try:
                    self.put_data_to_q(self.data_save_q, item)
                except Exception, e:
                    print('error : put queue error ')
                    print(e.message)
                print(u"put queue over")
            else:
                print(u"url:{} -->not find content".format(arcurl))
                print(u"content:{}".format(response.content))
        else:
            print(u"url: {} --->article respond is null !!".format(arcurl))

        return True

    def request(self, base_url, retries=3):

        if self.request_index[threading.currentThread().name] >= 15:  # request 循环 15 次 退出 request
            return None

        if retries < 0:
            self.__update_request()
            retries = 3

        proxies = {
            self.ip_data['type']: "{}://{}:{}".format(self.ip_data['type'], self.ip_data['ip'], self.ip_data['port'])}

        session = requests.session()
        session.keep_alive = False
        session.cookies = cookielib.LWPCookieJar(filename=self.__get_cookies_file())

        try:
            session.cookies.load(ignore_discard=True)
        except Exception as e:
            print u"session.cookies.load error : ", e.message

        try:
            print base_url, proxies
            respond = session.get(base_url, headers={"User-Agent": self.a_u}, timeout=5, proxies=proxies)
            if respond and respond.status_code == 200:  # 请求成功
                session.cookies.save()
                time.sleep(5)  # 请求 间隔
                print "get respond :", base_url
            elif respond.status_code == 407:  # # 请求失败 需要代理认证
                print 'proxy error :', respond.status_code
                self.put_data_to_q(self.ip_out_q, self.ip_data)  # # 舍弃 ip
                self.__update_request(2)  # 只需要 更改 代理 ip
                return self.request(base_url, retries)
            else:  # # 主要是 403 502 代理被封
                print 'error:'
                print respond.status_code, respond.reason, base_url
                time.sleep((4 - retries) * 5)
                self.__update_request()
                return self.request(base_url, retries-1)
        except Exception as e:
            if self.ip_sql.check_exception(e):  # # 代理 拒绝 或 连接 超时
                print 'proxy error \n', e.message
                self.put_data_to_q(self.ip_out_q, self.ip_data)  # # 舍弃 ip
                self.__update_request(2)
                return self.request(base_url, retries)
            elif "Connection aborted" in e.message:
                self.__update_request(0)
                return self.request(base_url, retries - 1)
                pass
            else:
                print u"无法连接网络 ！！！"
                print e.message
                time.sleep(5)
                if retries <= 1:
                    exit('无法连接网络 ！！！')
                return self.request(base_url, retries - 1)
        return respond

    def __get_cookies_file(self):
        name = threading.currentThread().name
        cookies_file_form = self.project_path + "/cache/{}_cookies"
        return cookies_file_form.format(name)

    def __update_request(self, update_type=1):
        self.request_index[threading.currentThread().name] += 1
        cookies_file_path = self.__get_cookies_file()

        if update_type == 1:  # # 全部 更换
            # 重新 设置 cookies
            with open(cookies_file_path, 'w') as f:
                f.write("")
            session = requests.session()
            session.keep_alive = False
            session.cookies = cookielib.LWPCookieJar(filename=cookies_file_path)
            header = {
                "Host": "www.toutiao.com",
                "User-Agent": self.a_u
            }
            session.get("http://www.toutiao.com/", headers=header, timeout=10)
            session.cookies.save()
            # 重新 设置 代理
            self.a_u = random.choice(agent)
            self.ip_data = self.get_data_from_q(self.ip_in_q)
        elif update_type == 2:  # 只需要 更改 代理 ip
            self.ip_data = self.get_data_from_q(self.ip_in_q)
            pass
        elif update_type == 3:  # 遇到 Connection aborted 情况
            pass
        else:   # 遇到 Connection aborted 情况
            with open(cookies_file_path, 'w') as f:
                f.write("")

    # 代理 ip 输入  ---> 解决mysql 多线程 问题
    def ip_in_work(self):
        while os.path.exists(self.pid_file_path) and self.pid == self.get_pid_str():
            if self.ip_sql.totalip() >= 1:
                if not self.ip_in_q.full():
                    self.ip_in_q.put_nowait(self.ip_sql.getrandomip())
                else:
                    print u"ip in queue is full !!! sleep 10s"
                    time.sleep(10)
            else:
                exit('mysql 中已经没有 ip 可以 用')
        pass

    # 无效 ip 出口
    def ip_out_work(self):
        while os.path.exists(self.pid_file_path) and self.pid == self.get_pid_str():
            if not self.ip_out_q.empty():
                item = self.ip_out_q.get_nowait()
                self.ip_sql.disableip(item.get('ip'))
            else:
                print u"ip out queue is full !!! sleep 20s "
                time.sleep(5)

    # 数据 存储
    def data_save_work(self):
        print u'queue_work'
        # del pid 强制结束
        index = 1
        while os.path.isfile(self.pid_file_path) and self.pid == self.get_pid_str():
            print u"当前线程数：", threading.active_count()
            if not self.data_save_q.empty():
                item = self.data_save_q.get_nowait()

                res = self.__ling_post(u"http://localhost:8082/addArticle", item)
                time.sleep(1)
                print u"save response:", res
                if res.get('status_code') == 200:
                    self.ssdb.request('set', [item['source_url'], item.get('group_id')])
                    self.ssdb.request('expire', [item['source_url'], 60 * 60 * 24 * 1])  # 1天有效期
                else:
                    print 'error !!!  无法 保存 数据！！！！'
                    self.del_pid_file()
                index = 1
            else:
                index += 1
                print u'no item sleep 3s'
                time.sleep(3)
                if index >= 20 or threading.active_count() <= 4:
                    self.del_pid_file()
        self.del_pid_file()
        print 'data_save_work queue is over'
        print u"当前线程数: {}".format(threading.active_count())

    # 将 数据 放入 队列
    def put_data_to_q(self, q, data, tries=20):  # data_queue ip_out_queue
        if tries <= 0:
            print q
            exit(u'put_data_to_q 无法 向队列 put 数据')
        if q.full():
            print u'put_data_to_q queue is empty so sleep 5s '
            self.put_data_to_q(q, data, tries-1)
        else:
            q.put_nowait(data)

    def get_data_from_q(self, q, tries=20):     # # q_in_queue
        if tries <= 0:
            print q
            exit(u'get_data_from_q 无法 获取队列数据')
        if q.empty():
            print u'get_data_from_q queue is empty so sleep 5s '
            self.get_data_from_q(q, tries-1)
        else:
            return q.get_nowait()

    def __ling_post(self, url, params):
        res = {}
        try:
            response = requests.post(url, params, timeout=61)
            res['status_code'] = response.status_code
            try:
                data = json.loads(response.content)
                pass
            except Exception, e:
                data = {u"message": u'error: try json.loads(response.content) ->{}'.format(e.message)}
                res['status_code'] = 110110
            res['reason'] = response.reason
            res['message'] = data.get('message')
            res['result'] = data.get('result')
            if response.status_code != 200:
                res['body'] = response.content
        except Exception, e:
            res['status_code'] = 110
            res['message'] = u"error:post  e.message->{}".format(e.message)
            res['url'] = url
        return res

    def __del__(self):
        self.del_pid_file()
        self.ssdb.close()
        self.ip_sql = None
        print '__del__ --> TouTiaoSpiderOne'

if __name__ == "__main__":
    a = TTSpider()
    a.run()
























