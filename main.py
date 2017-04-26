# _*_ encoding=utf-8 _*_

import requests
import json
from bs4 import BeautifulSoup

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

first_list_url = 'http://www.toutiao.com/api/pc/feed/?category=news_hot&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=false'


title_list_url = 'http://www.toutiao.com/api/pc/feed/?category=news_hot&utm_source=toutiao&widen=1&max_behot_time=%s&max_behot_time_tmp=%s&tadrequire=false'

url = title_list_url % ('1493193588', '1493193588')
print url

title_list_respond = requests.get(url)

with open('title_list_content.txt', 'w') as f:
    f.write(title_list_respond.content)

first_list_respond = requests.get(first_list_url)
print first_list_respond.status_code, first_list_respond.reason
first_list_content = json.loads(first_list_respond.content)
# print first_list_content['data']    # data
max_behot_time = first_list_content['next']['max_behot_time']
print 'max_behot_time' , first_list_content['next']     # max_behot_time

with open('first_list_content.txt', 'w') as f:
    f.write(first_list_respond.content)
index1 = 1
for item in first_list_content['data']:
    print item.get('has_gallery')
    print item.get('source_url')
    if item.get('has_gallery') == 'True':
        continue
    if item.get('source_url') == '':
        continue
    article_url = ''.join([domain, item.get('source_url')])
    print article_url
    article_respond = requests.get(article_url)
    with open('article_content%s.html' % (index1), 'w') as f:
        f.write(article_respond.content)
    soup = BeautifulSoup(article_respond.content, 'html.parser')
    header = soup.select('header > h1')
    print 'bb'
    if not header or len(header):
        print 'aa'
        header = soup.find('h1', class_='article-title')

    print header
    article = soup.find('article')
    if not article or len(article):
        article = soup.find_all('figure')
    print article
    print "\n"

print title_list_url % (max_behot_time, max_behot_time)






