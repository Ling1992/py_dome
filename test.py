# _*_ encoding=utf-8 _*_

from bs4 import BeautifulSoup
import json
import re
from get_article import MysqlLing

with open('title_list_content.html','r') as f:
    soup = BeautifulSoup(f, 'html.parser')
    header = soup.select('header > h1')
    if not header or not len(header):
        print 'header if 1'
        header = soup.find('h1', class_='article-title')
    else:
        header = header[0]
    if not header or not len(header):
        print 'header if 2'
        header = soup.find('h1')
    if not header or not len(header):
        raise Exception('header is none or []')
    header, number = re.subn("'", "\\'", str(header))
    print header
    article = soup.find('article')
    if not article or not len(article):
        print 'article if 1'
        figure = soup.find_all('figure')
        article = ''
        for i in figure:
            article = ''.join([article, str(i)])
    if not article or not len(article):
        print 'article if 2'
        article = soup.find('div', class_='article-content')
    if not article or not len(article):
        print 'article if 3'
        div = soup.find('div', class_='text')
        p = div.find_all('p')
        article = ''
        for i in p:
            article = ''.join([article, str(i)])
    if not article or not len(article):
        raise Exception('article is none or []')
    print article
    article, number = re.subn("'", "\\'", str(article))



