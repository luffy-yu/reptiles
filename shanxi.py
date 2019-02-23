#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
山西省政府采购
'''

import common
from bs4 import BeautifulSoup
import mysqlop

class ShanXi():
    _url = 'http://www.ccgp-shanxi.gov.cn/view.php?app=page&type=1&nav=100&page='
    _baseurl = 'http://www.ccgp-shanxi.gov.cn/'
    _initpagenum = 1
    _maxpagenum = 5
    _title = u'山西省政府采购'
    # if not exists 在python中执行总是有警告
    _createtable = 'create table if not exists shanxi(' \
                   'id int not null PRIMARY  KEY auto_increment,' \
                   'time date,' \
                   'title text,' \
                   'url text,' \
                   'reserved1 int,' \
                   'reserved2 text) DEFAULT CHARSET=utf8;'
    _insertor = u"insert into shanxi(time,title,url) " \
              " VALUES('{0}','{1}','{2}');"
    def __init__(self):
        print 'Get Data from http://www.ccgp-shanxi.gov.cn'
    def title(self):
        '''
        返回发送邮件时的标题
        :return:u'山西省政府采购'
        '''
        return self._title
    def getContent(self):
        cn = common.Common()
        ret = []
        try:
            for i in range(self._initpagenum,self._maxpagenum + 1,1):
                html = cn.getHtml(self._url + str(i))
                soup = BeautifulSoup(html,'html5lib')
                # print soup.prettify()
                trs = soup.select('#node_list tbody tr')
                # print len(trs)
                for tr in trs:
                    i = 0
                    for td in tr:
                        i += 1
                        if i == 1:
                            href = td.a['href']
                            title = td.a['title']
                            #process url
                            url = self._baseurl + href
                            continue
                        if i == 2:
                            #省本级
                            continue
                        if i == 3:
                            #招标中
                            continue
                        if i == 4:
                            #时间
                            time = td.string
                            #[2017-03-10]
                            time = str(time).replace('[','').replace(']','')
                            break
                    # print title,url,time
                    ret.append({'time': time, 'title': title, 'url': url})
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
    sx = ShanXi()
    ret = sx.getContent()
    # print sx.format(ret)
    sx.save2mysql(ret,"reptiles")
    # for i in ret:
    #     print  u"时间：" + i['time'] + i['title'] + i['url']