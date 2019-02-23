#!/usr/bin/env python
# -*- coding: utf-8 -*-

import common
from bs4 import BeautifulSoup
import mysqlop

class ShaanXi():
    _url = 'http://www.ccgp-shaanxi.gov.cn/saveData.jsp?ClassBID=C0001&type=AllView'
    _baseurl = 'http://www.ccgp-shaanxi.gov.cn/'
    _title = u'陕西省政府采购'
    _createtable = 'create table if not exists shaanxi(' \
                   'id int not null PRIMARY  KEY auto_increment,' \
                   'time date,' \
                   'title text,' \
                   'url text,' \
                   'reserved1 int,' \
                   'reserved2 text) DEFAULT CHARSET=utf8;'
    _insertor = u"insert into shaanxi(time,title,url) " \
              " VALUES('{0}','{1}','{2}');"
    _refer = 'http://www.ccgp-shaanxi.gov.cn/'
    _host = 'www.ccgp-shaanxi.gov.cn'
    def __init__(self):
        print 'Get Data from http://www.ccgp-shaanxi.gov.cn'
    def title(self):
        return self._title
    def getContent(self):
        cn = common.Common()
        ret = []
        try:
            # html = cn.getHtmlAsBrowser(self._url,self._refer,self._host)
            html = cn.getHtml(self._url)
            soup = BeautifulSoup(html,'html5lib')
            trs = soup.select('table .tab tbody tr .xian')
            # print len(trs)
            isodd = True
            #因为有循环，故先初始化变量
            title = None
            url = None
            time = None
            for tr in trs:
                if isodd:#奇数行
                    href =  tr.a['href']#链接
                    url = self._baseurl + href
                    title =  tr.a.string.strip()
                else:#偶数行
                    time = tr.string.replace('[','').replace(']','') #时间[2017-03-10]
                if not isodd :#偶数行之后存储记录
                    ret.append({'time': time, 'title': title, 'url': url})
                isodd = not isodd
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
    sn = ShaanXi()
    ret = sn.getContent()
    print sn.format(ret)
    sn.save2mysql(ret,"reptiles")