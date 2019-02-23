#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/10 下午4:42
# @Author  : Luffy
# @Site    : 
# @File    : mysqlop.py
# @Software: PyCharm Community Edition

'''
mysql数据库操作类
'''

import MySQLdb

#以下代码解决因中文出现的问题
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class MysqlOp():
    _host = ''
    _port = 3306
    _user = ''
    _pass = ''
    _db = ''
    _default_host = '127.0.0.1'
    _default_port = 3306
    _default_user = 'root'
    _default_pass = '123456'
    _default_db = 'mysql'
    def __int__(self):
        print 'MySQL operator class.'
    def set(self,host,user,passwd,db):
        self._host = host
        self._user = user
        self._pass = passwd
        self._db = db
    def loadDefault(self):
        self._host = self._default_host
        self._user = self._default_user
        self._pass = self._default_pass
        self._port = self._default_port
        self._db = self._default_db
    def connect(self):
        db = MySQLdb.connect(self._host,
                             self._user,
                             self._pass,
                             self._db,
                             charset='utf8',
                             #省略下一句会报错
                             #_mysql_exceptions.OperationalError: (2002, "Can't connect to local MySQL server through socket '/tmp/mysql.sock' (2)")
                             unix_socket='/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock')
        return db
    def runNotQuery(self,sql):
        ret = True
        try:
            db = self.connect()
            # mysql 5.1 会有编码问题，5.7不会有这么问题
            # db.set_character_set('utf8')
            # print 'character:',db.character_set_name()
            # db.set_character_set('utf8')
            # cursor = db.cursor()
            # cursor.execute('SET NAMES utf8;')
            # cursor.execute('SET CHARACTER SET utf8;')
            # cursor.execute('SET character_set_connection=utf8;')
            cursor = db.cursor()
            cursor.execute(sql)
            # ret = cursor.fetchall()
            db.commit()# If query,this line is not needed
            # print ret
            cursor.close()
            db.close()
        except Exception as e:
            ret = str(e)
        return ret
    def havedb(self,dbname):
        self.loadDefault()
        db = self.connect()
        cursor = db.cursor()
        sql = "SELECT count(*) FROM information_schema.SCHEMATA where SCHEMA_NAME='{0}'".format(dbname)
        cursor.execute(sql)
        ret = cursor.fetchone()
        cursor.close()
        db.close()
        if ret[0] == 1:
            return True
        else:
            return False
    def createdb(self,dbname):
        if self.havedb(dbname):
            self._db = dbname
            return True
        ret = True
        try:
            db = self.connect()
            cursor = db.cursor()
            # if not exists 语句在这里会报异常
            # sql = "CREATE DATABASE IF NOT EXISTS {0} default charset utf8 COLLATE utf8_general_ci;".format(dbname)
            sql = "CREATE DATABASE {0} default charset utf8 COLLATE utf8_general_ci;".format(dbname)
            cursor.execute(sql)
        except Exception as e:
            ret = str(e)
        # ret = cursor.fetchall()
        self._db = dbname
        return ret

    def test(self):
        self.loadDefault()
        db = self.connect()
        cursor = db.cursor()
        cursor.execute('select version()')
        data = cursor.fetchone()
        print 'Database version: ',data
        cursor.close()
        db.close()

if __name__ == '__main__':
    mo = MysqlOp()
    # mo.set('127.0.0.1','root','123456','test')
    # mo.loadDefault()
    mo.test()
    ret = mo.createdb("test1")
    # # ret = mo.havedb("reptiles")
    # ret = mo.createdb("reptiles")
    # sql = u"insert into shanxi(time,title,url)  VALUES('2017-03-10','山西省图书馆2017-2018年度安保服务项目采购招标公告','http://www.ccgp-shanxi.gov.cn/view.php?nid=285400');"
    # mo.runNotQuery("use reptiles;")
    # ret = mo.runNotQuery(sql,True)
    # mo.runNotQuery("commit;")
    # print ret