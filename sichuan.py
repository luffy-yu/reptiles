#!/usr/bin/env python
# -*- coding: utf-8 -*-

import common
from bs4 import BeautifulSoup
import mysqlop


class SiChuan():
    _url = 'http://www.sczfcg.com/CmsNewsController.do?' \
           'method=recommendBulletinList&moreType=' \
           'provincebuyBulletinMore&channelCode=cggg&rp=25&page=1'
    _baseurl = 'http://www.sczfcg.com'
    _title = u'四川省政府采购'
    _createtable = 'create table if not exists sichuan(' \
                   'id int not null PRIMARY  KEY auto_increment,' \
                   'time date,' \
                   'title text,' \
                   'url text,' \
                   'reserved1 int,' \
                   'reserved2 text) DEFAULT CHARSET=utf8;'
    _insertor = u"insert into sichuan(time,title,url) " \
                " VALUES('{0}','{1}','{2}');"

    # _refer = ''
    # _host = ''
    def __init__(self):
        print 'Get Data from http://www.sczfcg.com'

    def title(self):
        return self._title

    def getContent(self):
        cn = common.Common()
        ret = []
        try:
            html = cn.getHtml(self._url)
            soup = BeautifulSoup(html, 'html5lib')
            lis = soup.select(".colsList li")
            for li in lis:
                href =li.a['href']
                title = li.a['title']
                time = li.span.text
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
    sc = SiChuan()
    ret = sc.getContent()
    print sc.format(ret)
    sc.save2mysql(ret,"reptiles")