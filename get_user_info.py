# -*- coding: utf-8 -*-
import re
import demjson
import os
from base_class.ling_request import LingRequest
import sys
import MySQLdb
reload(sys)
sys.setdefaultencoding("utf-8")

sys.path.append("/Users/ling/PycharmProjects/py")
from collect_ip.ip_mysql import IpMysql

reg = re.compile(r'userInfo[\s]*=[\s]*{?[^}]*};?')
reg1 = re.compile(r'riot.mount[\s\S]{0,3}statistics[\s\S]?,{[^}]*}\);')
reg2 = re.compile(r'{[^}]*}')


class MysqlLing(object):
    db = None
    cursor = None
    __instance = None

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(MysqlLing, cls).__new__(cls, *args, **kwargs)
            cls.db = MySQLdb.connect("119.23.212.58", "ling", "LING-ling110412", "ling_index", charset="utf8")
            cls.cursor = cls.db.cursor()
            print 'MysqlLing __new__ '
        return cls.__instance

    def insert(self, sql_str):
        # print sql_str
        try:
            self.cursor.execute(sql_str)
            # insert_id = self.db.insert_id()
            # insert_id = self.cursor.lastrowid
            self.db.commit()
            return True
        except Exception, e:
            print e
            self.db.rollback()
            print 'rollback'
            return False

    def count(self, sql_str):
        count = self.cursor.execute(sql_str)
        return count

    def search(self, sql_str):
        print sql_str
        data = []
        try:
            self.cursor.execute(sql_str)
            results = self.cursor.fetchall()
            for row in results:
                author_id = row[0]
                name = row[1]
                media_id = row[2]
                fensi = row[3]
                guanzhu = row[4]
                author_type = row[5]
                data.append({'author_id': author_id, 'name': name, 'media_id': media_id, 'fensi': fensi, 'guanzhu': guanzhu, 'type': author_type})
        except Exception, e:
            print e
        return data

    def __del__(self):
        self.cursor.close()
        self.db.close()
        print 'db closed !'


def update(item):
    try:
        """
            sql 操作
        """
        print item
        ling_con = MysqlLing()
        ling_con.insert(
            "UPDATE toutiao_author SET name='%s', media_id='%s', fensi='%s', guanzhu='%s', type='%s', url='%s' where author_id='%s' "
            %
            (item['name'], item['mediaId'], item['fensi'], item['guanzhu'], item['type'], item['avatarUrl'], item['id'])
        )
    except Exception as e:
        print e


if __name__ == '__main__':
    current_pid = os.getpid()
    with open('cache/get_user_info.pid', 'w') as f:
        f.write('{}'.format(os.getpid()))

    base_url = "http://www.toutiao.com/c/user/{}/"
    ip_sql = IpMysql({'db': 'python_bases'})
    ling_con = MysqlLing()
    ling_request = LingRequest()
    author_list = ling_con.search("select * from toutiao_author where media_id=0")

    if len(author_list) >= 1:
        for author in author_list:
            user_id = author['author_id']
            respond = ling_request.request(base_url.format(user_id))
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
                if user['avatarUrl'].find('//') is 0:
                    user['avatarUrl'] = "http:" + user['avatarUrl']
                else:
                    pass
                update(user)
            else:
                # time.sleep(5)
                continue
            # time.sleep(0.5)
            pass
        pass

    if os.path.isfile('cache/get_user_info.pid'):
        os.remove('cache/get_user_info.pid')

