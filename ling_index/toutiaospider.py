# -*- coding: utf-8 -*-
from py_class.lingspider import LingSpider
import os


class TouTiaoSpider(LingSpider):
    category_content = {"behot_time": 0, "for_times": for_times, "model": model, "over": False}
    category = {
        # "news_tech": category_content,  # 科技
        # "news_entertainment": category_content,  # 娱乐
        # "news_sports": category_content,  # 体育
        "news_hot": category_content,  # 热点
        # "news_society": category_content,  # 社会
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
    }

    def __init__(self):
        LingSpider.__init__(self, os.path.basename(__file__))

    def start(self):
        print 'TouTiaoSpider start !!!'
        self.ling_request('aaa')
    pass


