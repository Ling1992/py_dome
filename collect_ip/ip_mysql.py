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
            print 'rollback'
            return False
