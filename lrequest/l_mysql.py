# -*- coding: UTF-8 -*-
import MySQLdb


class LMysql(object):
    db = None
    cursor = None
    __instance = None

    def __init__(self, *args):
        print "l_ mysql init  "
        pass

    def __new__(cls, *args):
        if not cls.__instance:
            cls.__instance = super(LMysql, cls).__new__(cls, *args)
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

    def count(self, sql_str):
        count = self.cursor.execute(sql_str)
        return count

    def disable_ip(self, ip):
        try:
            self.cursor.execute(
                "UPDATE pi_pool SET state = 1 WHERE ip = '{}'"
                .format(ip))
            self.db.commit()
        except Exception, e:
            print 'IpMysql updatedisableip error:'
            print e
            self.db.rollback()

    def get_random_ip(self):
        data = {}
        try:
            self.cursor.execute("SELECT "
                                "* FROM pi_pool AS t1 "
                                "JOIN "
                                "( "
                                "SELECT ROUND( RAND( ) * "
                                "( "
                                "( SELECT MAX( id ) FROM pi_pool WHERE state = 0 ) - "
                                "( SELECT MIN( id ) FROM pi_pool WHERE state = 0 ) "
                                ") + "
                                "( SELECT MIN( id ) FROM pi_pool WHERE state = 0 ) ) AS id "
                                ") "
                                "AS t2 "
                                "WHERE t1.id >= t2.id "
                                "AND t1.state = 0 "
                                "ORDER BY t1.id "
                                "LIMIT 1")
            results = self.cursor.fetchall()
            for row in results:
                data['id'] = row[0]
                data['ip'] = row[1]
                data['port'] = row[2]
                data['type'] = "http" if row[3] == 1 else "https"
        except Exception, e:
            print 'IpMysql getrandomip error:'
            print e
        return data

    def __del__(self):
        self.cursor.close()
        self.db.close()
        print 'db closed !'


if __name__ == '__main__':
    mysql = LMysql({'db': 'python_bases'})


