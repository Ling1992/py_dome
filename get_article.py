# -*- coding: UTF-8 -*-

import MySQLdb


class MysqlLing(object):
    db = None
    __instance = None

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(MysqlLing, cls).__new__(cls, *args, **kwargs)
            cls.db = MySQLdb.connect("localhost", "root", "root", "ling_python_test1", charset="utf8")
        return cls.__instance

    def __del__(self):
        self.db.close()
        print 'db closed !'


if __name__ == '__main__':

    # ling = MysqlLing()
    # cursor = ling.db.cursor()
    #
    # sql = "insert into article(title, article) values ('%s', '%s') " % ('test_title ', '啊哈哈哈哈')
    #
    # try:
    #     cursor.execute(sql)
    #     ling.db.commit()
    # except:
    #     ling.db.rollback()

    aa = 'asdlfjasl%sasdfla%ss'
    bb = aa % ('埃里克森的', '说了打飞机阿里圣诞节')
    print aa
    print bb

