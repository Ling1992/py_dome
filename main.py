# _*_ encoding=utf-8 _*_

import requests


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

title_list_url = 'http://www.toutiao.com/api/pc/feed/?category=news_hot&utm_source=toutiao&widen=1&max_behot_time=1493016519&max_behot_time_tmp=1493016519&tadrequire=true&as=A16518DFBD3A23C&cp=58FD7AC2437C6E1'





