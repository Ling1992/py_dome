# _*_ encoding=utf-8 _*_

from bs4 import BeautifulSoup
import json
import re
from get_article import MysqlLing

# with open('title_list_content.html', 'r') as f:
#     soup = BeautifulSoup(f, 'html.parser')
#     header = soup.select('header > h1')
#     if not header or not len(header):
#         print 'header if 1'
#         header = soup.find('h1', class_='article-title')
#     else:
#         header = header[0]
#     if not header or not len(header):
#         print 'header if 2'
#         header = soup.find('h1')
#     if not header or not len(header):
#         raise Exception('header is none or []')
#     header, number = re.subn("'", "\\'", str(header))
#     print header
#     article = soup.find('article')
#     if not article or not len(article):
#         print 'article if 1'
#         figure = soup.find_all('figure')
#         article = ''
#         for i in figure:
#             article = ''.join([article, str(i)])
#     if not article or not len(article):
#         print 'article if 2'
#         article = soup.find('div', class_='article-content')
#     if not article or not len(article):
#         print 'article if 3'
#         div = soup.find('div', class_='text')
#         p = div.find_all('p')
#         article = ''
#         for i in p:
#             article = ''.join([article, str(i)])
#     if not article or not len(article):
#         raise Exception('article is none or []')
#     print article
#     article, number = re.subn("'", "\\'", str(article))



item = {'image_url': 'http://p1.pstatp.com/list/190x124/18a5000442ebc3d519e8', 'is_feed_ad': False, 'tag_url': 'search/?keyword=%E5%85%B6%E5%AE%83', 'title': '\u4eba\u771f\u7684\u80fd\u9884\u611f\u81ea\u5df1\u7684\u6b7b\u4ea1\u5417\uff1f', 'tag': 'news', 'single_mode': True, 'abstract': '\u53ef\u80fd\u771f\u7684\u6709\u9884\u611f\uff0c\u6211\u524d\u6bb5\u65f6\u95f4\u4e70\u83dc\u4e86\uff0c\u548c\u6211\u8001\u516c\u5c31\u65e9\u4e0a\u665a\u4e0a\u6709\u7a7a\u8bf4\u8bdd\uff0c\u6211\u8001\u516c\u4eca\u5e74\u6b6340\u5c81\uff0c\u4ec0\u4e48\u75c5\u4e5f\u6ca1\u6709\uff0c\u80fd\u5403\u80fd\u559d\u7684\u5e72\u6d3b\u4e5f\u884c\uff0c\u5c31\u5728\u4e09\u6708\u4e8c\u5341\u53f7\u90a3\u5929\u65e9\u4e0a\u4ed6\u8bf4:\u5ab3\u5987\u6211\u91cc\u8fb9\u75bc\u4e0d\u662f\u4ec0\u4e48\u597d\u4e8b\u3002\u4ed6\u8bf4\u5b8c\uff0c\u6211\u5c31\u9a82\u4ed6\u522b\u653e\u5c41\uff0c\u6211\u63a5\u7740\u8bf4\u54b1\u53bb\u533b\u9662\u67e5\u67e5\u53bb\uff0c\u4ed6\u662f\u6b7b\u6d3b\u4e0d\u53bb\uff0c\u8bf4\u5c31\u75bc\u4e00.', 'middle_mode': False, 'behot_time': 1493704207, 'chinese_tag': '\u5176\u5b83', 'source': '\u5934\u6761\u95ee\u7b54', 'more_mode': True, 'article_genre': 'article', 'comments_count': 384, 'image_list': [{'url': 'http://p1.pstatp.com/list/18a5000442ebc3d519e8'}, {'url': 'http://p3.pstatp.com/list/18a400020903105560f1'}, {'url': u'http://p3.pstatp.com/list/1a6c0009ae06198d1466'}], 'group_source': 10, 'has_gallery': False, 'source_url': '/group/6402119330049294593/', 'group_id': '6402119330049294593'}


regex = re.compile(r'^search/\?')
m = regex.match("aaaa")
if m:
    print m.group()
else:
    print 'not find'
print item['tag_url']


