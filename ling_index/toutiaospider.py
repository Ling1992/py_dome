# -*- coding: utf-8 -*-
from py_class.lingspider import LingSpider
import re
import os
import time
import threading
from pyquery import PyQuery as pq


class TouTiaoSpider(LingSpider):
    threads = [
        "news_hot",
        "news_tech"
    ]

    # "news_hot": category_content,  # 热点
    # "news_society": category_content,  # 社会
    # "news_entertainment": category_content,  # 娱乐
    # "news_tech": category_content,  # 科技
    # "news_sports": category_content,  # 体育
    # "news_car": category_content,  # 汽车
    # "news_finance": category_content,  # 财经
    # "funny": category_content,  # 搞笑
    # "news_military": category_content,  # 军事
    # "news_fashion": category_content,  # 时尚
    # "news_discovery": category_content,  # 探索
    # "news_regimen": category_content,  # 养生
    # "news_essay": category_content,  # 美文
    # "news_history": category_content,  # 历史
    # "news_world": category_content,  # 国际
    # "news_travel": category_content,  # 旅游
    # "news_baby": category_content,  # 育儿
    # "news_story": category_content,  # 故事
    # "news_game": category_content,  # 游戏
    # "news_food": category_content,  # 美食


    api_url = "http://www.toutiao.com/api/pc/feed/?category={0}&utm_source=toutiao&widen=1&max_behot_time={1}&max_behot_time_tmp=0&tadrequire=false&as=A175990077EECF2&cp=59078EBCCFF2DE1"

    for_times_model_one = 1
    for_times_model_two = 1
    index = {}
    behot_time = {}
    url = {}
    for_time = 2 * 24 * 60 * 60  # 两天秒数
    for_time1 = 5 * 60  # 两天秒数
    sample_interval = 5*60  # 5分钟 间隔
    model = {}
    is_model_four = False

    reg = re.compile(r'[0-9]+')  # "media_url": "/c/user/5739097906/",

    def __init__(self, model):
        LingSpider.__init__(self, os.path.basename(__file__))
        for t in self.threads:
            self.behot_time[t] = 0
            self.index[t] = None
            self.url[t] = None
            self.model[t] = model
        print u'TouTiaoSpider -> init'

    def spider(self):

        # model one behot_time=0 当前时间 遍历 所有栏目 10次
        # model two behot_time取每次请求返回的值 遍历所有栏目 10次
        # # model one 和 two 是白天 模式 定时时间 10分钟 一次
        # model three behot_time 每次时间戳减5*60s 获取最近两天数据
        # model four behot_time 每次时间戳减5*60s 获取历史两天数据 (history_time.txt)
        # # model three 和 four 是 夜间模式 定时时间 1小时一次

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
        elif model[0] == 'three':
            if index is None:
                index = self.for_time1
                behot_time = int(time.time())
            else:
                index -= self.sample_interval
                behot_time -= self.sample_interval

            if index <= 0:
                del model[0]
                index = None
        elif model[0] == 'four':
            print 'four1'
            if index is None:
                print 'four2'
                index = self.for_time
                try:
                    with open('cache/history_time.txt', 'r+') as f:
                        history_time = f.read()
                except Exception, e:
                    print e.message
                    history_time = None
                if history_time:
                    behot_time = int(time.mktime(time.strptime(history_time, "%Y-%m-%d %H:%M:%S")))  # 2017-05-08 00:00:00
                else:
                    behot_time = int(time.time()) + (60 * 60)
                if self.is_model_four is False:
                    with open('cache/history_time.txt', 'w') as f:
                        self.is_model_four = True
                        f.write(time.strftime("%Y-%m-%d 00:00:00", time.localtime(behot_time - 60 * 60 * 24 * 2)))
            else:
                index -= self.sample_interval
                behot_time -= self.sample_interval

            if index <= 0:
                print 'four3'
                del model[0]
                index = None
        else:
            return False
        self.model[name] = model
        self.index[name] = index
        self.behot_time[name] = behot_time
        self.log(model,u"ling -->循环模式")
        self.log(index, u"ling --> 循环次数")
        print u"behot_time: ", behot_time
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
            self.log(e.message)
            self.behot_time[name] = behot_time
            return None

        # 文章获取
        if arclist and len(arclist) >= 1:
            for data in arclist:
                res = self.get_article(data)
                if res is not True:
                    return res

    def save(self, item):
        self.log(item)

    def get_article(self, data):
        item = {}
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
