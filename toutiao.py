# -*- coding: utf-8 -*-

import cookielib
import random
import time
import json
import re
import requests
import threading
import Queue
from pyquery import PyQuery as pq
from base_class.ling_mysql import MysqlLing
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# key 专题 { behot_time 需保存的参数behot_time   for_times 最大循环次数  model 模式 }
#       -->模式1 : behot_time 一直为0 ,模式2 : behot_time 取每次请求返回的值 ,
#       模式3 behot_time 每次时间戳减10*60s 获取最近两天数据 模式4 : behot_time 每次时间戳减5*60s 获取历史两天数据

model = 1
for_times = 60
category_content ={"behot_time": 0, "for_times": for_times, "model": model, "over": False}
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
q = Queue.Queue(128)

apiurl = "http://www.toutiao.com/api/pc/feed/?category={0}&utm_source=toutiao&widen=1&max_behot_time={1}&max_behot_time_tmp=0&tadrequire=false&as=A175990077EECF2&cp=59078EBCCFF2DE1"
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

http = ['119.5.1.13:808', '218.22.219.133:808', '183.78.183.156:82', '218.64.37.70:8118', '116.199.115.78:80']
# https = ['112.193.91.55:80', '222.89.102.6:808', '119.48.181.236:8118', '119.96.203.368118', '115.202.162.65:808']
regex = re.compile(r'^/api/')  # url = '/api/pc/subject/6417225587135349249/'
reg = re.compile(r'[0-9]+')  # "media_url": "/c/user/5739097906/",


def ttrequsts(url, **args):
    name = threading.current_thread().name
    print 'category:{} url:{}'.format(name, url)
    header = {
        # "HOST": "www.toutiao.com", # 解决 301 重定向问题
        "Referfer": "www.toutiao.com",
        "User-Agent": random.choice(agent)
    }
    proxies = {
        'http': 'http://{}'.format(random.choice(http))
        # 'https': 'https://{}'.format(random.choice(https))
    }
    print header['User-Agent']
    # 默认的是FileCookieJar没有实现save函数。
    # 而MozillaCookieJar或LWPCookieJar都已经实现了。
    # 所以可以用MozillaCookieJar或LWPCookieJar，去自动实现cookie的save。
    # 实现，通过文件保存cookie。
    # 建议用LWPCookieJar，其保存的cookie，易于人类阅读
    session = requests.Session()
    session.cookies = cookielib.LWPCookieJar(filename="cache/toutiao_{}_cookies.txt".format(name))
    try:
        # ignore_discard=True 忽略关闭浏览器丢失 , ignore_expires=True ,忽略失效  --load() 在文件中读取cookie
        session.cookies.load(ignore_discard=True)
    except:
        print u"failed load cookie"
    time.sleep(6)  # 请求 时间 间隔
    try:
        response = session.get(url, headers=header, timeout=10, **args)
        session.cookies.save()
    except Exception as e:
        print e
        return None
    if response and response.status_code == 200:
        return response
    print response.status_code, response.reason


def start():
    global category
    name = threading.current_thread().name
    current_time = None  # 模式3 专用 时间戳 递减 记录
    # time_total = (365*24*60*60/2)  # 半年时间
    time_total = 2 * 24 * 60 * 60    # 时间
    time_sample = {3: 60 * 10, 4: 60 * 5}   # 模式3 10分钟 模式4 5分钟时间间隔 秒

    if category[name]['model'] == 3:
        category[name]['for_times'] = time_total
    elif category[name]['model'] >= 4:
        return False
    elif category[name]['model'] <= 0:
        return False

    while 1:

        print 'model:', category[name]['model']
        print 'for_times:', category[name]['for_times']
        if category[name]['model'] >= 3:
            if current_time is None:
                if category[name]['model'] == 3:
                    current_time = int(time.time())
                else:
                    with open('history_time.txt', 'r') as f:
                        history_time = f.read()
                    if history_time:
                        current_time = int(time.mktime(time.strptime(history_time, "%Y-%m-%d %H:%M:%S")))  # 2017-05-08 00:00:00
                        with open('history_time.txt', 'w') as f:
                            f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time - 60 * 60 * 24 * 2)))
                    else:
                        break
            else:
                current_time -= time_sample[category[name]['model']]

            behot_time = current_time
        elif category[name]['model'] == 2:
            behot_time = category[name]['behot_time']
        else:
            behot_time = 0

        print '线程: {} ;be hot time :{}'.format(name, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(behot_time)))
        # python从2.6开始支持format
        # data = {'first': 'Hodor', 'last': 'Hodor!'}
        # Old
        # '%(first)s %(last)s' % data
        # New
        # '{first} {last}'.format(**data)
        # Output
        # Hodor Hodor!

        url = apiurl.format(name, behot_time)

        # print "{0}==={1}".format(name, url)

        response = ttrequsts(url)
        if response is not None:
            log('list_url : {}'.format(url))
            log('list_request_code : {}, list_request_message : {}'.format(response.status_code, response.reason))
            log('list_request_content : {}'.format(response.content))
            arclist = parselist(response)
            if len(arclist) > 0:
                crawlarc(arclist)

        if category[name]['for_times'] <= 0:
            if category[name]['model'] >= 4:
                break
            else:
                category[name]['model'] += 1
                current_time = None
                if category[name]['model'] >= 3:
                    category[name]['for_times'] = time_total
                else:
                    category[name]['for_times'] = for_times
        else:
            if category[name]['model'] >= 3:
                category[name]['for_times'] -= time_sample[category[name]['model']]
            else:
                category[name]['for_times'] -= 1

    category[name]['over'] = True

def parselist(response):
    name = threading.current_thread().name
    json = response.json()
    print 'next>>>>>>>>>>>{0}'.format(json["next"]["max_behot_time"])
    global category
    category[name]['behot_time'] = json["next"]["max_behot_time"]
    arclist = [item for item in json["data"]
               if item["article_genre"] == "article"
               and item["source"] != u"头条问答"
               and not regex.match(item['source_url'])]
    return arclist


def crawlarc(alist):
    for data in alist:
        item = {}
        import urlparse
        arcurl = urlparse.urljoin("http://www.toutiao.com", data["source_url"])
        arcres = ttrequsts(arcurl)
        if arcres is not None:
            log('article_url : {}'.format(arcurl))
            log('article_request_code : {}, article_request_message : {}'.format(arcres.status_code, arcres.reason))

            title, number = re.subn("'", "\\'", str(data["title"]))  # 解决 单引号 插入数据库 出错问题
            item["title"] = title
            item["tag"] = data["tag"]
            item["chinese_tag"] = data.get('chinese_tag')
            item["url"] = arcurl
            item["group_id"] = data["group_id"]
            item["original_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data["behot_time"]))
            m = reg.search(data.get('media_url'))
            if m:
                item['author_id'] = m.group()
            else:
                item['author_id'] = 46543

            text = unicode(arcres.content, encoding='utf-8')  # 解决乱码问题
            dom = pq(text).make_links_absolute(arcres.url)
            content = dom.find(".article-content").html()

            if not content or not len(content):
                content = dom('article').html()
            if not content or not len(content):
                content = dom.find(".text").html()
            if not content or not len(content):
                content = dom.find(".contentMain").html()
            if not content or not len(content):
                print 'content:{}'.format(repr(content))
                if data["source"] == u"专题":
                    print '专题跳过'
                    continue
                else:
                    # raise Exception('content is null !!')
                    print 'content is null 跳过 !! url:{}  content:{}  dom:{}'.format(arcurl, content, dom)
                    log('content is null 跳过 !! url:{}  content:{}  dom:{}'.format(arcurl, content, dom), key_str='ling')
                    continue
            content, number = re.subn("\r", "\n", str(content))  # 解决 \r 插入数据库 值为空的问题
            content, number = re.subn("'", "\\'", str(content))  # 解决 单引号 插入数据库 出错问题
            item['content'] = content
            q.put(item)
        else:
            print 'article respond is null !!'
            continue


def log(content, key_str='default'):
    with open('cache/{}_at_{}.log'.format(threading.current_thread().name, time.strftime("%Y-%m-%d", time.localtime(time.time()))), 'a') as f:
        f.write('{} -->>'.format(key_str))
        f.write('{}:\n'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))))
        f.write('\t')
        # f.write(repr(content))
        f.write(json.dumps(content, ensure_ascii=False, encoding='utf-8'))
        f.write('\n')


def q_work():
    is_over = True

    while is_over or q.qsize() >= 1:
        item = q.get()
        save(item)

        for (key, value) in category.iteritems():
            is_over = value['over'] and is_over
        is_over = not is_over
        pass
    print 'queue size: ', q.qsize()
    for (key, value) in category.iteritems():
        print 'category:{} , is_over:{}'.format(key, value['over'])
    print 'queue is over'


def save(item):
    print "\n{0}--thread is working>>>>>>>>>>>>>>>>>>>>>\n".format(threading.currentThread().getName())
    try:
        # import json
        # css = pq(response.text).make_links_absolute(response.url)
        # data["content"] = css.find(".article-content").html()
        # res = requests.post("http://192.168.10.254:5678/index.php/xsapi/ucsave", data={"data": json.dumps(data)})
        # print res.text
        """
            sql 操作
        """
        ling_con = MysqlLing()
        """
        count = ling_con.count("select * from article_list where url='%s'"
                               %
                               item['url']
                               )
        print count
        if count:
            print '数据 重复！！！'
        else:
            print '新增 数据 ！！！'
            res = ling_con.insert(
                "insert into article_list(title, tag, chinese_tag, url, group_id, original_time) "
                "VALUES "
                "('%s', '%s', '%s', '%s', '%s', '%s')"
                %
                (item['title'], item['tag'], item['chinese_tag'], item['url'], item['group_id'], item['original_time'])
            )
            print res
            if res:
                pass
            else:
                raise Exception('insert article_list error ')
            res = ling_con.insert("INSERT INTO article(url, title, article) "
                                  "VALUES "
                                  "('%s', '%s', '%s')"
                                  %
                                  (item['url'], item['title'], item['content'])
                                  )
            print res
            if res:
                print 'insert article success !!'
            else:
                raise Exception('insert article error ')

        print "\n"
        """
        count = ling_con.count("select * from author_list where id='%s'"
                               %
                               item['author_id']
                               )
        if count:
            pass
        else:
            print 'insert author_list'
            ling_con.insert(
                "insert into author_list(id) VALUES ('%s')" % (item['author_id'])
            )
    except Exception as e:
        print e
        pass


if __name__ == "__main__":

    threads = []
    # 队列
    tf = threading.Thread(target=q_work, name='queue')
    threads.append(tf)

    for _, v in category.iteritems():
        tf = threading.Thread(target=start, name=_)
        threads.append(tf)

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print 'game over'

