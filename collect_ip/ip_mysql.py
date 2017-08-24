# -*- coding: UTF-8 -*-
import sys
sys.path.append("/Users/ling/PycharmProjects/py_dome/")
from base_class.base_mysql import MysqlBase


class IpMysql(MysqlBase):

    def delip(self, ip):
        try:
            self.cursor.execute(" DELETE from  pi_pool where id = {}".format(ip))
            self.db.commit()
            return True
        except Exception, e:
            print e
            self.db.rollback()
            print 'rollback delip'
            return False

    def totalall(self):
        total = 100000
        try:
            self.cursor.execute("SELECT COUNT(*) FROM pi_pool")
            total = self.cursor.fetchone()[0]
        except Exception, e:
            print 'IpMysql total error:'
            print e
        return total

    def totalofdisabelip(self):
        total = 0
        try:
            self.cursor.execute("SELECT COUNT(*) FROM pi_pool WHERE state = 1 ")
            total = self.cursor.fetchone()[0]
        except Exception, e:
            print 'IpMysql totalofdisabelip error:'
            print e
        return total

    def save(self, data):
        if self.haveip(data['ip']) == 0:
            try:
                self.cursor.execute(" INSERT INTO pi_pool(ip, port, type) VALUE('{}', {}, {})"
                                    .format(data['ip'], data['port'], data['type']))
                self.db.commit()
            except Exception, e:
                print e
                print data
                print 'rollback save'
                self.db.rollback()

    def updatedisableip(self, data):
        if self.haveip(data['ip']) == 0:
            try:
                self.cursor.execute("SELECT id from pi_pool WHERE state = 1 LIMIT 1")
                ip_id = self.cursor.fetchone()[0]
                self.cursor.execute(
                    "UPDATE pi_pool SET ip = '{}', port = {}, type = {}, state = 0 WHERE id = {}"
                    .format(data['ip'], data['port'], data['type'], ip_id))
                self.db.commit()
            except Exception, e:
                print 'IpMysql updatedisableip error:'
                print e
                self.db.rollback()

    def disableip(self, ip):
        try:
            self.cursor.execute(
                "UPDATE pi_pool SET state = 1 WHERE ip = '{}'"
                .format(ip))
            self.db.commit()
        except Exception, e:
            print 'IpMysql updatedisableip error:'
            print e
            self.db.rollback()

    def getrandomip(self):
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

    def totalip(self):
        pass

    def haveip(self, ip):
        try:
            res = self.cursor.execute(" SELECT * FROM pi_pool WHERE ip='{}'".format(ip))
            return res
        except Exception, e:
            print 'IpMysql haveip error'
            print e
            return False

