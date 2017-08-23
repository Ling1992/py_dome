# -*- coding: UTF-8 -*-

import MySQLdb


class MysqlBase(object):
    db = None
    cursor = None
    __instance = None

    def __init__(self, *args):
        pass

    def __new__(cls, *args):
        if not cls.__instance:
            cls.__instance = super(MysqlBase, cls).__new__(cls, *args)
            if args:
                params = args[0]
            else:
                params = {}
            print params

            cls.db = MySQLdb.connect(params.get('ip') if params.get('ip') else "localhost",
                                     params.get('user') if params.get('user') else "root",
                                     params.get('pwd') if params.get('pwd') else "root",
                                     params.get('db') if params.get('db') else "test", charset="utf8")
            cls.cursor = cls.db.cursor()
            print 'MysqlLing __new__ '
        return cls.__instance

    def insert(self, sql_str):
        # print sql_str
        try:
            self.cursor.execute(sql_str)
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

    def __del__(self):
        self.cursor.close()
        self.db.close()
        print 'db closed !'


if __name__ == '__main__':
    mysql = MysqlBase({'db': 'python_bases'})


