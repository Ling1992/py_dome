# -*- coding: UTF-8 -*-
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

    def total(self):
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
        pass
