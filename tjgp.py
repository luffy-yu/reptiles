#!/usr/bin/env python
# -*- coding: utf-8 -*-

import common
from bs4 import BeautifulSoup
import mysqlop

class Tjgp():
    _url = 'http://www.tjgp.gov.cn/portal/topicView.do?method=view&view=Infor&id=1665&ver=2&st=1'
    _baseurl = 'http://www.tjgp.gov.cn'
    _title = u'天津市政府采购'
    _createtable = 'create table if not exists tjgp(' \
                   'id int not null PRIMARY  KEY auto_increment,' \
                   'time date,' \
                   'title text,' \
                   'url text,' \
                   'reserved1 int,' \
                   'reserved2 text) DEFAULT CHARSET=utf8;'
    _insertor = u"insert into tjgp(time,title,url) " \
              " VALUES('{0}','{1}','{2}');"
    _month_num = {
        'Jan':1,
        'Feb':2,
        'Mar':3,
        'Apr':4,
        'May':5,
        'Jun':6,
        'Jul':7,
        'Aug':8,
        'Sept':9,
        'Oct':10,
        'Nov':11,
        'Dec':12
    }
    # _refer = ''
    # _host = ''
    def __init__(self):
        print 'Get Data from http://www.tjgp.gov.cn'
    def title(self):
        return self._title
    def getContent(self):
        cn = common.Common()
        ret = []
        try:
            html = cn.getHtml(self._url)
            soup = BeautifulSoup(html,'html5lib')
            lis = soup.select("#div_ul_1 li")
            for li in lis:
                href = li.a['href']
                url = self._baseurl + href
                title = li.a['title']
                time = li.span.string#Fri Mar 10 20:25:39 CST 2017
                time = self.formatTime(time)#2017-3-10
                ret.append({'time': time, 'title': title, 'url': url})
        except Exception as e:
            print str(e)
        return ret
    def formatTime(self,str):#Fri Mar 10 20:25:39 CST 2017 --> 2017-3-10
        list = str.split(" ")
        if len(list) < 6:
            return str
        return "{0}-{1}-{2}".format(list[5],self._month_num[list[1]],list[2])


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
    tj = Tjgp()
    ret = tj.getContent()
    print tj.format(ret)
    tj.save2mysql(ret,"reptiles")