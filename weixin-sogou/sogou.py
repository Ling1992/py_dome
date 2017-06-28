# -*- coding: utf-8 -*-
import requests
import cookielib
import random
import time
import Queue
import re
from pyquery import PyQuery as pq
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

url = u'http://weixin.sogou.com/pcindex/pc/pc_4/1.html'
url = u'http://weixin.sogou.com/pcindex/pc/pc_4/pc_4.html'

url = u'http://weixin.sogou.com/pcindex/pc/pc_{0}/{1}.html'
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
save_q = Queue.Queue(128)
reg_video = re.compile(r'video_iframe')


def work():
    items = request_list(url.format(0, 'pc_0'))
    if items:
        for item in items:
            # request_author(item)
            request_article(item)
            if item['article_content']:
                save(item)
    pass


def request_author(item):
    response = ling_request(item['account_url'])
    if response:
        dom = get_dom(response)
        item['profile_nickname'] = dom.find('.profile_nickname').text()
        profile_account = dom.find('.profile_account').text()
        profile_account = profile_account.replace(u'微信号: ', u'')
        profile_account = profile_account.replace(u'微信号:', u'')
        item['profile_account'] = profile_account
        if not profile_account:
            print u'cannot get author info !!'
    pass


def request_article(item):
    item['article_content'] = None
    response = ling_request(item['article_url'])
    if response:
        m = reg_video.search(response.content)
        if m:
            print u'reg_video !!'
            pass
        else:
            dom = get_dom(response)
            content = dom.find('.rich_media_content').html()
            content, number = re.subn("\r", "", str(content))  # 解决 \r 插入数据库 值为空的问题
            content, number = re.subn("'", "\\'", str(content))  # 解决 单引号 插入数据库 出错问题
            item['article_content'] = content
    pass


def save(item):
    print u'item:', item
    pass


def request_list(request_url):
    article_list = []
    response = ling_request(request_url)
    if response:
        dom = get_dom(response)
        if dom:
            lis = dom('li')
            for li in lis.items():
                item = {}
                # title
                title = li.find('.txt-box').find('h3').find('a').text()
                item['title'] = title
                # article_summary
                article_summary = li.find('.txt-box').find('p[class=txt-info]').text()
                item['article_summary'] = article_summary
                # article_url
                article_url = li.find('.txt-box').find('h3').find('a').attr('href')
                item['article_url'] = article_url
                # time
                original_time = li.find('.s-p').attr('t')
                if not original_time:
                    print u'original_time 1'
                    original_time = li.find('.s2').attr('t')
                item['original_time'] = original_time
                # image url
                image = li.find('.img-box').find('img').attr('src')
                item['image'] = image
                # account url
                account_url = li.find('.account').attr('href')
                item['account_url'] = account_url
                # account i
                account_i = li.find('.account').attr('i')
                item['account_i'] = account_i
                article_list.append(item)
    return article_list
    pass


def get_dom(response):
    dom = None
    try:
        text = unicode(response.content, encoding='utf-8')  # 解决乱码问题
        dom = pq(text)
    except Exception, e:
        print u'get_dom fail!! Exception:', e
    return dom
    pass


def ling_request(request_url):
    response = None
    print request_url
    headers = {
        "Referfer": "http://weixin.sogou.com/",
        "User-Agent": random.choice(agent)
    }
    session = requests.session()
    session.cookies = cookielib.LWPCookieJar(filename='cache/py_class/cookies.log')
    try:
        session.cookies.load(ignore_discard=True)
    except Exception, e:
        print u'load fail cookies ！！ Exception:', e
    try:
        response = session.get(request_url, headers=headers, timeout=10)
        session.cookies.save()
        time.sleep(1)
        print response.status_code, response.reason
    except Exception, e:
        print u' request get fail !! Exception: ', e
    if response and response.status_code == 200:
        return response


if __name__ == '__main__':
    work()
    pass

