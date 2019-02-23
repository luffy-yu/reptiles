#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/13 下午4:44
# @Author  : Luffy
# @Site    : 
# @File    : hainan.py
# @Software: PyCharm Community Edition

import common
from bs4 import BeautifulSoup
import mysqlop


class HaiNan():
    _url = u'http://www.ccgp-hainan.gov.cn/cgw/cgw_list.jsp?bid_type=101&zone=%E7%9C%81%E6%9C%AC%E7%BA%A7'
    _baseurl = 'http://www.ccgp-hainan.gov.cn'
    _title = u'海南省政府采购'
    _createtable = 'create table if not exists hainan(' \
                   'id int not null PRIMARY  KEY auto_increment,' \
                   'time date,' \
                   'title text,' \
                   'url text,' \
                   'reserved1 int,' \
                   'reserved2 text) DEFAULT CHARSET=utf8;'
    _insertor = u"insert into hainan(time,title,url) " \
                " VALUES('{0}','{1}','{2}');"

    # _refer = ''
    # _host = ''
    def __init__(self):
        print 'Get Data from http://www.ccgp-hainan.gov.cn'

    def title(self):
        return self._title

    def getContent(self):
        cn = common.Common()
        ret = []
        try:
            html = cn.getHtml(self._url)
            soup = BeautifulSoup(html, 'html5lib')
            lis = soup.select(".nei02_04_01 li")
            for li in lis:
                title = li.em.text.strip()
                href = li.em.a['href']
                time = li.i.text
                url = self._baseurl + href
                ret.append({'time': time, 'title': title, 'url': url})
        except Exception as e:
            print str(e)
        return ret

    def format(self, ret):
        '''
        格式化输出
        :param ret:爬去的内容
        :return:格式化后的输出
        '''
        str = ""
        for i in ret:
            str += u'时间：{0} <a href="{1}">{2}</a><br>'.format(i['time'], i['url'], i['title'])
        return str

    def save2mysql(self, data, dbname):
        ret = True
        try:
            mo = mysqlop.MysqlOp()
            mo.loadDefault()
            mo.createdb(dbname)
            mo.runNotQuery(self._createtable)
            for dat in data:
                sql = self._insertor.format(dat['time'], dat['title'], dat['url'])
                mo.runNotQuery(sql)
        except Exception as e:
            ret = str(e)
        return ret


if __name__ == '__main__':
    hn = HaiNan()
    ret = hn.getContent()
    print hn.format(ret)
    hn.save2mysql(ret,"reptiles")