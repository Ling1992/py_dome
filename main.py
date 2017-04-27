# _*_ encoding=utf-8 _*_

import requests
from bs4 import BeautifulSoup
from get_article import MysqlLing
import time
import json

domain = 'http://www.toutiao.com'

domain_respond = requests.get(domain)
"""
    首页 找出 需要的数据
"""

with open('domain_content.html', 'w') as f:
    f.write(domain_respond.content)

heard_list_url = 'http://s3a.pstatp.com/toutiao/resource/ntoutiao_web/page/home/whome/home_465fa88.js'

heard_list_respond = requests.get(heard_list_url)
"""
    .js 文件的处理
"""
with open('heard_list_content.txt', 'w') as f:
    f.write(heard_list_respond.content)


# 热点
title_url = '/ch/news_hot/'

print ''.join([domain, title_url])


title_respond = requests.get(''.join([domain, title_url]))

title_list_url = 'http://www.toutiao.com/api/pc/feed/?category=news_hot&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A11539D0713B436&cp=59013B14E316DE1'

url = title_list_url

while 1:
    print url
    title_list_respond = requests.get(url)
    print title_list_respond.status_code, title_list_respond.reason
    if title_list_respond.status_code != 200:
        break
    title_list_content = json.loads(title_list_respond.content)
    behot_time = title_list_content['next']['max_behot_time']
    url = title_list_url
    print 'max_behot_time' , title_list_content['next']     # max_behot_time

    for item in title_list_content['data']:
        print 'has_gallery', item.get('has_gallery')
        print 'source_url:', item.get('source_url')
        if item.get('has_gallery'):
            continue
        if item.get('source_url') == '':
            continue
        article_url = ''.join([domain, item.get('source_url')])
        print article_url
        article_respond = requests.get(article_url)
        print article_respond.status_code
        if article_respond.status_code != 200:
            continue
        """
            bs4 html 操作
        """
        soup = BeautifulSoup(article_respond.content, 'html.parser')
        header = soup.select('header > h1')
        if not header or not len(header):
            print 'header if 1'
            header = soup.find('h1', class_='article-title')
        else:
            header = header[0]
        if not header or not len(header):
            raise Exception('header is none or []')

        print header
        article = soup.find('article')
        if not article or not len(article):
            print 'article if 1'
            article = soup.find_all('figure')
        if not article or not len(article):
            print 'article if 2'
            article = soup.find('div', class_='article-content')
        if not article or not len(article):
            raise Exception('article is none or []')
        print article

        """
            sql 操作
        """
        ling_con = MysqlLing()
        count = ling_con.count("select * from article_list where group_id='%s'"
                               % item.get('group_id'))
        print count
        if count:
            print '数据 重复！！！'
            res = False
        else:
            print '新增 数据 ！！！'
            res = ling_con.insert("insert into article_list(title, abstract, tag, group_id, original_time) VALUES ('%s', '%s', '%s', '%s', '%s')"
                            % (item.get('title'), item.get('abstract'), item.get('tag'), item.get('group_id'), item.get('behot_time')))
            print res
            if res:
                pass
            else:
                raise Exception('insert article_list error ')
            res = ling_con.insert("INSERT INTO article(article_id, title, article) VALUES ('%s', '%s', '%s')"
                                  % (item.get('group_id'), header, article))
            print res
            if res:
                print 'insert article success !!'
            else:
                raise Exception('insert article error ')

        print "\n"
        time.sleep(1)
    time.sleep(2)







