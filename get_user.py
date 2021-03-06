# -*- coding: utf-8 -*-
import requests
import random
import cookielib
import re
import demjson
import time
from base_class.ling_mysql import MysqlLing

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
reg = re.compile(r'userInfo[\s]*=[\s]*{?[^}]*};?')
reg1 = re.compile(r'riot.mount[\s\S]{0,3}statistics[\s\S]?,{[^}]*}\);')
reg2 = re.compile(r'{[^}]*}')


def save(item):
    try:
        """
            sql 操作
        """
        ling_con = MysqlLing()
        count = ling_con.count("select * from toutiao_author where id='%s'"
                               %
                               item['id']
                               )
        print count
        if count:
            print '数据 重复！！！'
        else:

            res = ling_con.insert(
                "insert into toutiao_author(id, name, media_id, fensi, guanzhu, type) "
                "VALUES "
                "('%s', '%s', '%s', '%s', '%s', '%s')"
                %
                (item['id'], item['name'], item['mediaId'], item['fensi'], item['guanzhu'], item['type'])
            )
            # print res
            if res:
                print '新增 数据 ！！！'
                pass
            else:
                print 'insert author error '
        print "\n"

        if item['mediaId'] > 0:
            count = ling_con.count("select * from toutiao_author where id='%s'"
                                   %
                                   item['id']
                                   )
            if count:
                pass
            else:
                ling_con.insert(
                    "insert into toutiao_author(id, name, media_id, fensi, guanzhu, type) "
                    "VALUES "
                    "('%s', '%s', '%s', '%s', '%s', '%s')"
                    %
                    (item['id'], item['name'], item['mediaId'], item['fensi'], item['guanzhu'], item['type'])
                )

    except Exception as e:
        print e
        pass

if __name__ == '__main__':
    print __name__

    # get session
    session = requests.session()
    session.cookies = cookielib.LWPCookieJar(filename="cache/domain.txt")
    header = {
        "Host": "www.toutiao.com",
        "User-Agent": random.choice(agent)
    }
    respond = session.get("http://www.toutiao.com/", headers=header, timeout=10)
    session.cookies.save()

    base_url = "http://www.toutiao.com/c/user/{}/"
    with open('get_user_id.txt', 'r') as f:
        user_id = int(f.read())
    print user_id
    index = 0
    while 1:
        header = {
            "Host": "www.toutiao.com",
            "User-Agent": random.choice(agent)
        }
        try:
            session.cookies.load(ignore_discard=True)
        except Exception as e:
            print e
            raise Exception('session.cookies.load error ')

        try:
            respond = session.get(base_url.format(user_id), headers=header, timeout=10)
            session.cookies.save()
        except Exception as e:
            print e
            raise Exception(' request get  fail  session.get(base_url.format(user_id), headers=header, timeout=10)')

        if respond and respond.status_code == 200:
            print "get respond"
        else:
            print respond.status_code, respond.reason
            raise Exception('session.get(base_url.format(user_id), headers=header, timeout=10) error ')

        s = reg.search(respond.content)
        s1 = reg1.search(respond.content)
        if s and s1:
            content, number = re.subn("\r", "", str(reg2.search(s.group()).group()))
            content, number = re.subn("\n", "", content)
            user1 = demjson.decode(content)

            content, number = re.subn("\r", "", str(reg2.search(s1.group()).group()))
            content, number = re.subn("\n", "", content)
            user2 = demjson.decode(content)
            user = dict(user1.items() + user2.items())
            save(user)
            print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            print user_id
            with open('get_user_id.txt', 'w') as f:
                f.write(str(user_id))
            # print user
        else:
            continue
        time.sleep(1)
        index += 1
        if index > 1000:
            break

