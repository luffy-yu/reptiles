#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/14 下午3:08
# @Author  : Luffy
# @Site    : 
# @File    : bjcz.py
# @Software: PyCharm Community Edition

import common
from bs4 import BeautifulSoup
import mysqlop
import re


class Bjcz():
    _url = 'http://www.bjcz.gov.cn/zfcgcs/bjszfcgggcs/syzbggcs/index.htm'
    _baseurl = 'http://www.bjcz.gov.cn'
    _title = u'北京市政府采购（北京财政局）'
    _createtable = 'create table if not exists bjcz(' \
                   'id int not null PRIMARY  KEY auto_increment,' \
                   'time date,' \
                   'title text,' \
                   'url text,' \
                   'reserved1 int,' \
                   'reserved2 text) DEFAULT CHARSET=utf8;'
    _insertor = u"insert into bjcz(time,title,url) " \
                " VALUES('{0}','{1}','{2}');"

    # _refer = ''
    # _host = ''
    def __init__(self):
        print 'Get Data from http://www.bjcz.gov.cn'

    def title(self):
        return self._title

    def getContent(self):
        cn = common.Common()
        ret = []
        try:
            html = cn.getHtml(self._url)
            soup = BeautifulSoup(html, 'html5lib')
            # print html
            trs = soup.select("table tbody tr td table tbody tr")
            for tr in trs:
                if tr.a.string is None:
                    continue
                title = tr.a.string.strip()
                href = re.search(r"/\w+.+htm",tr.a['href']).group(0)
                if href is None:
                    continue
                time = tr.contents[4].text.strip()
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
    bj = Bjcz()
    ret = bj.getContent()
    print bj.format(ret)
    bj.save2mysql(ret,"reptiles")