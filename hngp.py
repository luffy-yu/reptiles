#!/usr/bin/env python
# -*- coding: utf-8 -*-

import common
from bs4 import BeautifulSoup
import mysqlop

class Hngp():
    _url = 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=0101&bz=0&pageSize='
    _baseurl = 'http://www.hngp.gov.cn'
    _pageSize = 100
    _title = u'河南省政府采购'
    _createtable = 'create table if not exists hngp(' \
                   'id int not null PRIMARY  KEY auto_increment,' \
                   'time date,' \
                   'title text,' \
                   'url text,' \
                   'reserved1 int,' \
                   'reserved2 text) DEFAULT CHARSET=utf8;'
    _insertor = u"insert into hngp(time,title,url) " \
              " VALUES('{0}','{1}','{2}');"
    # _refer = ''
    # _host = ''
    def __init__(self):
        print 'Get Data from http://www.hngp.gov.cn'
    def title(self):
        return self._title
    def getContent(self):
        cn = common.Common()
        ret = []
        try:
            html = cn.getHtml(self._url + str(self._pageSize))
            soup = BeautifulSoup(html, 'html5lib')
            lis = soup.select(".List2 ul li")
            for li in lis:
                time = li.span.text
                href = li.a['href']
                url = self._baseurl + href
                title = li.a.text
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
    hn = Hngp()
    ret = hn.getContent()
    print hn.format(ret)
    hn.save2mysql(ret,"reptiles")