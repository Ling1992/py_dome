# -*- coding: utf-8 -*-

# 通过 作者 找文章
import Queue
import time
import threading
import random
import requests
import cookielib
import json
from pyquery import PyQuery as pq
import re
from base_class.ling_mysql import MysqlLing
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


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


# 从 .txt 中获取 作者 id
def init_author_id():
    author_ids = []
    with open('author.txt', 'r') as f:
        for line in f.readlines():
            author_ids.append(line.replace("\n", ''))

    return author_ids


# 把 id push 到队列中
def push_id(ids):
    for author_id in ids:
        id_q.put(author_id)


# 从队列中获取 author id
def get_id():
    index = 0
    while 1:
        try:
            author_id = id_q.get_nowait()
            return author_id
        except Exception as e:
            print 'get_id():', 'id 为空', e
            time.sleep(5)
            pass
        index += 1
        if index >= 10:
            print 'get_id() is over !!'
            return 0


# queue work  save data def
def q_save():
    while 1:
        flag = True
        try:
            item = save_q.get_nowait()
            save(item)
        except Exception as e:
            print 'q_save()', 'save_q 队列 为空', e
            time.sleep(5)
            pass
        for k, v in work_is_over.iteritems():
            flag = flag & v
        if flag:
            break
    print 'queue save data is over !!'


# save data def
def save(item):
    # mysql
    # print 'save def:', data
    try:
        """
            sql 操作
        """
        ling_con = MysqlLing()
        count = ling_con.count("select * from author_list where id='%s'"
                               %
                               item['author_id']
                               )
        if count:
            pass
        else:
            res = ling_con.insert(
                "insert into author_list(id, name) VALUES ('%s', '%s')" % (item['author_id'], item['source'])
            )
            if res:
                print '新增 author 数据 ！！！'
                pass
            else:
                print 'insert author error '

        count = ling_con.count("select * from article_list where url='%s'" % item['display_url'])
        # print count
        if count:
            pass
            # print '数据 重复！！！'
        else:
            print '新增 数据 ！！！'
            res = ling_con.insert(
                "insert into article_list(title, tag, chinese_tag, url, group_id, original_time, abstract, author_id) "
                "VALUES "
                "('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
                %
                (item['title'], item['tag'], item['chinese_tag'], item['display_url'], item['group_id'], item['original_time'], item['abstract'], item['author_id'])
            )
            print res
            if res:
                pass
            else:
                raise Exception('insert article_list error ')
            res = ling_con.insert("INSERT INTO article(url, title, article, author_id) "
                                  "VALUES "
                                  "('%s', '%s', '%s', '%s')"
                                  %
                                  (item['display_url'], item['title'], item['content'], item['author_id'])
                                  )
            print res
            if res:
                print 'insert article success !!'
            else:
                raise Exception('insert article error ')

    except Exception as e:
        print e
        pass

    # post url
    # r = requests.post("http://119.23.62.164:5757/index.php/xsapi/ucsave/", timeout=10, data={"data": json.dumps(item)})


# 统一 post data 格式
def filterwork(item):
    keymap = {'abstract': "desc", "tag": "tag", "title": "title", "chinese_tag": "chinese_tag", "source": "author", "comments_count": "comment_count", "source_url": "url", "behot_time": "behot_time"}
    return {keymap[key]: value for key, value in item.items() if key in keymap.keys()}


#  main work def
def work():
    base_url = 'http://www.toutiao.com/c/user/article/?page_type=1&user_id={0}&max_behot_time=0&count=20&as=A10599123FFA611&cp=592FFA9611B11E1'
    while 1:
        # 获取 author id
        author_id = get_id()
        # print 'work()', author_id
        # 判断 id 队列 是否 完全 为空
        if author_id == 0:
            work_is_over[int(threading.current_thread().name)] = True
            print '当前线程结束 :', threading.current_thread().name
            break
        # 存在 id 进行 爬取信息
        article_list = get_article_list(base_url.format(author_id))
        if article_list is not None:
            for article in article_list:
                article['author_id'] = author_id
                # 最近一天数据
                if article['behot_time'] >= int(time.time() - 24 * 60 * 60):
                    get_article(article)
                else:
                    print '过时 数据-->behot_time:', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(article["behot_time"]))
            pass
        else:
            continue

    print 'work is over !!'


# get about author article list info
def get_article_list(url):
    response = ling_request(url)
    if response is not None:
        response_dict = json.loads(response.content)
        article_list = response_dict["data"]
        if len(article_list) >= 1:
            lists = [item for item in article_list if item["article_genre"] == "article" and item["source"] != u"头条问答"]
            return lists
        else:
            return None
    else:
        return None


# get article
def get_article(item):
    if item['display_url']:
        url = item['display_url']
    else:
        url = u"http://toutiao.com/group/{}/".format(item['group_id'])
    response = ling_request(url)
    if response is not None:

        try:
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

            if content:
                content, number = re.subn("\r", "\n", str(content))  # 解决 \r 插入数据库 值为空的问题
                content, number = re.subn("'", "\\'", str(content))  # 解决 单引号 插入数据库 出错问题
                item['content'] = content
                item["original_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item["behot_time"]))
                print 'push save queue!!'
                save_q.put(item)
            else:
                print 'content:', content
                pass
        except Exception, e:
            print 'analyse article response error !!', e

    else:
        pass


def ling_request(url):
    # 请求 间隔
    time.sleep(5)
    name = threading.current_thread().name
    print 'current_thread Name:{} -->url:{}'.format(name, url)
    header = {
        "Referfer": "www.toutiao.com",
        "User-Agent": random.choice(agent)
    }
    session = requests.session()
    session.cookies = cookielib.LWPCookieJar(filename="toutiao2_thread{}_cookies.txt".format(name))
    try:
        session.cookies.load(ignore_discard=True)
    except Exception as e:
        print u"load cookies fail ", e
    try:
        response = session.get(url, headers=header, timeout=10)
        session.cookies.save()
    except Exception as e:
        print u"session.get(url) 请求失败 ！", e
        return None
    print response.status_code, response.reason
    if response and response.status_code == 200:
        # print response.text
        return response
    else:
        return None


if __name__ == '__main__':
    t_num = [1, 2, 3]
    threads = []
    work_is_over = {}
    for t in t_num:
        work_is_over[t] = False
    print work_is_over

    # author id 分发队列
    id_q = Queue.Queue()
    push_id(init_author_id())

    # save data 队列
    save_q = Queue.Queue(128)
    save_q_t = threading.Thread(target=q_save, name='save_t')
    threads.append(save_q_t)

    for t in t_num:
        print t
        work_t = threading.Thread(target=work, name=t)
        threads.append(work_t)

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print 'game over !!'



