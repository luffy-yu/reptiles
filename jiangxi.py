#!/usr/bin/env python
# -*- coding: utf-8 -*-

import common
from bs4 import BeautifulSoup
import mysqlop


class JiangXi():
    _url = 'http://ggzy.jiangxi.gov.cn/jxzbw/zfcg/017002/017002001/'
    _baseurl = 'http://ggzy.jiangxi.gov.cn'
    _title = u'江西省政府采购'
    _createtable = 'create table if not exists jiangxi(' \
                   'id int not null PRIMARY  KEY auto_increment,' \
                   'time date,' \
                   'title text,' \
                   'url text,' \
                   'reserved1 int,' \
                   'reserved2 text) DEFAULT CHARSET=utf8;'
    _insertor = u"insert into jiangxi(time,title,url) " \
                " VALUES('{0}','{1}','{2}');"

    # _refer = ''
    # _host = ''
    def __init__(self):
        print 'Get Data from http://ggzy.jiangxi.gov.cn'

    def title(self):
        return self._title

    def getContent(self):
        cn = common.Common()
        ret = []
        try:
            html = cn.getHtml(self._url)
            soup = BeautifulSoup(html, 'html5lib')
            tds = soup.select(".liebiaobg td")
            i = 0
            href = None
            title = None
            time = None
            for td in tds:
                i += 1
                if i == 1:#img标签，没用
                    continue
                if i == 2:#a标签，title和href
                    href = td.a['href']
                    url = self._baseurl + href
                    title = td.text.strip()
                    continue
                if i == 3:#时间，[2017-03-11]
                    time = td.text.replace('[','').replace(']','')
                    # print time,title,url
                    ret.append({'time': time, 'title': title, 'url': url})
                    i = 0
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
    jx = JiangXi()
    ret = jx.getContent()
    print jx.format(ret)
    jx.save2mysql(ret,"reptiles")