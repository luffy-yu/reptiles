#!/usr/bin/env python
# -*- coding: utf-8 -*-

import common
from bs4 import BeautifulSoup
import mysqlop
import re


class QingHai():
    _url = 'http://www.ccgp-qinghai.gov.cn/jilin/zbxxController.form?declarationType=GKZBGG&pageNo=0&type=1'
    _baseurl = ''
    _title = u'青海省政府采购'
    _createtable = 'create table if not exists qinghai(' \
                   'id int not null PRIMARY  KEY auto_increment,' \
                   'time date,' \
                   'title text,' \
                   'url text,' \
                   'reserved1 int,' \
                   'reserved2 text) DEFAULT CHARSET=utf8;'
    _insertor = u"insert into qinghai(time,title,url) " \
                " VALUES('{0}','{1}','{2}');"

    # _refer = ''
    # _host = ''
    def __init__(self):
        print 'Get Data from http://www.ccgp-qinghai.gov.cn'

    def title(self):
        return self._title

    def getContent(self):
        cn = common.Common()
        ret = []
        try:
            html = cn.getHtml(self._url)
            soup = BeautifulSoup(html, 'html5lib')
            # print html
            lis = soup.select(".m_list_3 li")
            for li in lis:
                newsdate = li.span.text#2017年03月13日
                match = re.findall(r"\d{1,4}",newsdate)
                time = "{0}-{1}-{2}".format(match[0],match[1],match[2])
                title = str(li.a['title']).strip()
                url = li.a['href']
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
    qh = QingHai()
    ret = qh.getContent()
    print qh.format(ret)
    qh.save2mysql(ret,"reptiles")