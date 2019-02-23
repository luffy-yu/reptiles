#!/usr/bin/env python
# -*- coding: utf-8 -*-

import common
from bs4 import BeautifulSoup
import mysqlop
import re


class ZheJiang():
    _url = 'http://www.zjzfcg.gov.cn/new/articleSearch/search_search.do?count=30&bidType=11&region=339900&chnlIds=207,211&bidMenu=&searchKey=&bidWay=&applyYear=2017&flag=1&releaseStartDate=&noticeEndDate=&releaseEndDate=&noticeEndDate1=&zjzfcg=0'
    _baseurl = 'http://www.zjzfcg.gov.cn/new'
    _title = u'浙江省政府采购'
    #没有发布时间，只有截至时间，相应的建表语句和插入语句发生变化
    _createtable = 'create table if not exists zhejiang(' \
                   'id int not null PRIMARY  KEY auto_increment,' \
                   'time date,' \
                   'title text,' \
                   'url text,' \
                   'endtime date,' \
                   'reserved2 text) DEFAULT CHARSET=utf8;'
    _insertor = u"insert into zhejiang(title,url,endtime) " \
                " VALUES('{0}','{1}','{2}');"

    # _refer = ''
    # _host = ''
    def __init__(self):
        print 'Get Data from http://www.zjzfcg.gov.cn'

    def title(self):
        return self._title

    def getContent(self):
        cn = common.Common()
        ret = []
        try:
            html = cn.getHtml(self._url)
            soup = BeautifulSoup(html, 'html5lib')
            lis = soup.select("#tigtag2_right li")
            for li in lis:
                for child in li.children:
                    # print child.name
                    name = child.name
                    if name == "span":
                        time = child.text#[截止:2017-03-30]
                        endtime = re.search(r'\d{4}-\d{1,2}-\d{1,2}',time).group(0)
                        continue
                    if name == "a":
                        if child.has_attr('title'):
                            title = child['title']
                            href = child['href']
                            url = self._baseurl + str(href).replace("..","")
                # print title,url,endtime
                # break
                ret.append({'endtime': endtime, 'title': title, 'url': url})
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
            str += u'截至时间：{0} <a href="{1}">{2}</a><br>'.format(i['endtime'], i['url'], i['title'])
        return str

    def save2mysql(self, data, dbname):
        ret = True
        try:
            mo = mysqlop.MysqlOp()
            mo.loadDefault()
            mo.createdb(dbname)
            mo.runNotQuery(self._createtable)
            for dat in data:
                # sql = self._insertor.format(dat['time'], dat['title'], dat['url'])
                sql = self._insertor.format(dat['title'], dat['url'],dat['endtime'])
                mo.runNotQuery(sql)
        except Exception as e:
            ret = str(e)
        return ret

if __name__ == '__main__':
    zj = ZheJiang()
    ret = zj.getContent()
    print zj.format(ret)
    zj.save2mysql(ret,"reptiles")
