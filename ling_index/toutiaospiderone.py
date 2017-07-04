# -*- coding: utf-8 -*-
from py_class.lingspider import LingSpider
from py_class.SSDB import SSDB
import re
import os
import time
import threading
import requests
import json
from pyquery import PyQuery as pq


class TouTiaoSpiderOne(LingSpider):
    threads = [
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

    api_url = "http://www.toutiao.com/api/pc/feed/?category={0}&utm_source=toutiao&widen=1&max_behot_time={1}&max_behot_time_tmp=0&tadrequire=false&as=A175990077EECF2&cp=59078EBCCFF2DE1"

    for_times_model_one = 2
    for_times_model_two = 3
    index = {}
    behot_time = {}
    url = {}
    model = {}

    reg = re.compile(r'[0-9]+')  # "media_url": "/c/user/5739097906/",

    def __init__(self):
        LingSpider.__init__(self, os.path.basename(__file__))
        for t in self.threads:
            self.behot_time[t] = 0
            self.index[t] = None
            self.url[t] = None
            self.model[t] = ["one", "two"]
        self.ssdb = SSDB('127.0.0.1', 8888)
        print u'TouTiaoSpider -> init'

    def spider(self):

        # model one behot_time=0 当前时间 遍历 所有栏目 10次
        # model two behot_time取每次请求返回的值 遍历所有栏目 10次
        # # model one 和 two 是白天 模式 定时时间 10分钟 一次

        name = threading.currentThread().name
        model = self.model[name]
        index = self.index[name]
        behot_time = self.behot_time[name]

        # 处理 循环条件
        if model is None or len(model) <= 0:
            return False
        if model[0] == 'one':
            if index is None:
                index = self.for_times_model_one
                behot_time = 0
            else:
                index -= 1

            if index <= 0:
                del model[0]
                index = None
        elif model[0] == 'two':
            if index is None:
                index = self.for_times_model_two
                behot_time = 0
            else:
                index -= 1

            if index <= 0:
                del model[0]
                index = None
        else:
            return False
        self.model[name] = model
        self.index[name] = index
        self.behot_time[name] = behot_time
        print u"behot_time: ", behot_time
        print u"循环模式："
        print model
        self.log(model, u"ling -->循环模式")
        self.log(index, u"ling --> 循环次数")
        self.log(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(behot_time)), u"ling --> 循环时间戳")
        # 列表数据
        res, response = self.ling_request(self.api_url.format(name, behot_time))
        if res['status_code'] == 110:
            return False
        if res['status_code'] == 404:
            return None
        while res['status_code'] == 403:
            res, response = self.ling_request(self.api_url.format(name, behot_time))
            time.sleep(10)

        json = response.json()
        try:
            if len(model) >= 1 and model[0] == 'two':
                behot_time = json["next"]["max_behot_time"]
                self.behot_time[name] = behot_time

            arclist = [item for item in json["data"]
                       if (item["article_genre"] == "article" or item["article_genre"] == "gallery")
                       and item["source"] != u"头条问答" and item["source"] != u"专题"]
            self.log(arclist)
        except Exception, e:
            print u"article list 处理出现错误 ！！", e.message
            print u"article list: ", json['data']
            self.log(u"error:")
            self.log(e.message)
            return None

        # 文章获取
        if arclist and len(arclist) >= 1:
            for data in arclist:
                self.get_article(data)

    def save(self, item):
        res = self.__ling_post(u"http://localhost:8082/addArticle", item)
        if res['status_code'] != 200:
            time.sleep(10)
            res = self.__ling_post(u"http://localhost:8082/addArticle", item)
        return res

    def get_article(self, data):
        item = {}

        if data.get("source_url"):
            pass
        else:
            self.log(u'error:')
            self.log(data)
            return None

        res = self.ssdb.request('get', [data['source_url']])
        if res.code == 'ok':
            return None
        else:
            self.ssdb.request('set', [data['source_url'], data.get('group_id')])
            self.ssdb.request('expire', [data['source_url'], 60*60*24*10])  # 10天有效期

        arcurl = "http://www.toutiao.com{}".format(data["source_url"])
        res, response = self.ling_request(arcurl)

        if res['status_code'] == 110:
            return False
        if res['status_code'] == 404:
            return None
        while res['status_code'] == 403:
            res, response = self.ling_request(arcurl)
            time.sleep(20)

        if response is not None:
            text = unicode(response.content, encoding='utf-8')  # 解决乱码问题
            dom = pq(text).make_links_absolute(response.url)
            content = dom.find(".article-content").html()

            if not content or not len(content):
                content = dom('article').html()

            if not content or not len(content):
                content = dom.find('.article-main').html()

            if not content or not len(content):
                content = dom.find('.rich_media_content').html()

            if not content or not len(content):
                content = dom.find(".text").html()

            if not content or not len(content):
                content = dom.find(".contentMain").html()

            if not content or not len(content):
                content = dom.find('.textindent2em').html()

            if not content or not len(content):
                content = dom.find('.f14').html()

            if not content or not len(content):
                content = dom.find('.m-detail-bd').html()

            if not content or not len(content):
                content = dom.find('.artical-content').html()

            if content:
                # toutiao_article_category 分类 数据源
                item["category_word"] = data.get("tag")
                item["category_name"] = data.get('chinese_tag')
                # toutiao_article_0x 文章 数据源
                content, number = re.subn("\r", "\n", str(content))  # 解决 \r 插入数据库 值为空的问题
                content, number = re.subn("'", "\\'", str(content))  # 解决 单引号 插入数据库 出错问题
                item['article_content'] = content
                # toutiao_article_list 列表 数据源
                title, number = re.subn("'", "\\'", str(data.get("title")))  # 解决 单引号 插入数据库 出错问题
                item["title"] = title
                item['abstract'] = data.get('abstract')
                item['image_url'] = data.get('image_url')
                item["create_date"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data.get("behot_time")))
                item["url"] = response.url  # 文章url 重定向后 url //唯一性判断
                # toutiao_author 作者 数据源
                if data.get('media_url'):
                    m = self.reg.search(data.get('media_url'))
                    if m:
                        item['author_id'] = m.group()
                    else:
                        item['author_id'] = 0
                else:
                    item['author_id'] = 0

                self.log('push save queue!!')
                # 放入队列
                self.q.put(item)
            else:
                self.log(u"url:{} -->not find content".format(arcurl))
        else:
            self.log(u"url: {} --->article respond is null !!".format(arcurl))

        return True

    def __ling_post(self, url, params):
        res = {}
        try:
            response = requests.post(u"http://localhost:8082/addArticle", params, timeout=61)
            data = json.loads(response.content)
            res['status_code'] = response.status_code
            res['reason'] = response.reason
            res['message'] = data.get('message')
            res['result'] = data.get('result')
        except Exception, e:
            res['status_code'] = 110
            res['message'] = u"error:  e.message->{}".format(e.message)
            res['url'] = url
        self.log(res)
        return res

    def __del__(self):
        self.ssdb.close()

if __name__ == u"__main__":
    current_file = os.path.basename(__file__)
    (name, ext) = os.path.splitext(current_file)
    pid_file = u"cache/{}.pid".format(name)
    if not os.path.exists(pid_file):
        spider = TouTiaoSpiderOne()
        spider.run()
    else:
        print u"{}.pid 已经存在 ！！ 请及时处理！！".format(name)
