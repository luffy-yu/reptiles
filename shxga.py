#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/10 下午2:20
# @Author  : Luffy
# @Site    : 
# @File    : shxga.py
# @Software: PyCharm Community Edition

'''
爬取陕西省公安政府采购信息
'''

import common
from bs4 import BeautifulSoup
import mysqlop


class Shxga():
    '''
    爬取陕西省公安政府采购信息
    '''
    _url = "http://www.shxga.gov.cn/n17580/n17773/n18300/index.html"
    _baseurl = "http://www.shxga.gov.cn"
    _title = u'陕西省公安厅政府采购'
    _createtable = 'create table if not exists shxga(' \
                   'id int not null PRIMARY  KEY auto_increment,' \
                   'time date,' \
                   'title text,' \
                   'url text,' \
                   'reserved1 int,' \
                   'reserved2 text) DEFAULT CHARSET=utf8;'
    _insertor = u"insert into shxga(time,title,url) " \
              " VALUES('{0}','{1}','{2}');"

    def __init__(self):
        print 'Get Data from http://www.shxga.gov.cn'

    def title(self):
        '''
        返回发送邮件时的标题
        :return:u'陕西省公安厅政府采购'
        '''
        return self._title
    def getContent(self):
        '''
        爬取内容
        :return:内容
        '''
        cn = common.Common()
        html = cn.getHtml(self._url)
        soup = BeautifulSoup(html,'html5lib')
        # print soup.prettify()
        lis = soup.select(".news_list li")
        ret = []
        try:
            for li in lis:
                # print li.span.string #time
                time = li.span.string
                attrs = li.a.attrs
                href = self._baseurl + attrs['href']
                title = attrs['title']
                ret.append({'time':time,'title':title,'url':href})
        except Exception as e:
            print str(e)
        return ret
    def format(self,ret):
        '''
        格式化输出
        :param ret:爬去的内容
        :return:格式化后的输出
        '''
        str = ""
        for i in ret:
            str += u'时间：{0} <a href="{1}">{2}</a><br>'.format(i['time'],i['url'],i['title'])
        return str
    def save2mysql(self,data,dbname):
        ret = True
        try:
            mo = mysqlop.MysqlOp()
            mo.loadDefault()
            mo.createdb(dbname)
            mo.runNotQuery(self._createtable)
            for dat in data:
                sql = self._insertor.format(dat['time'],dat['title'],dat['url'])
                mo.runNotQuery(sql)
        except Exception as e:
            ret = str(e)
        return ret

if __name__ == '__main__':
    sa = Shxga()
    ret = sa.getContent()
    sa.save2mysql(ret,"reptiles")
    # print sa.format(ret)
    # for i in ret:
    #     print  u"时间：" + i['time'] + i['title'] + i['url']
    # import shxga
    # help(shxga)