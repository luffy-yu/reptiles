#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/13 下午1:27
# @Author  : Luffy
# @Site    : 
# @File    : shanghai.py
# @Software: PyCharm Community Edition

import common
from bs4 import BeautifulSoup
import mysqlop
import re

class ShangHai():
    _url = 'http://www.ccgp-shanghai.gov.cn/news.do?method=purchasePracticeMore'
    _baseurl = 'http://www.ccgp-shanghai.gov.cn/topubforward.do?method=forwordTo&url=/bulletin.do?method=bulletinbmindex@@bulletin_id={0}'
    _title = u'上海市政府采购'
    _createtable = 'create table if not exists shanghai(' \
                   'id int not null PRIMARY  KEY auto_increment,' \
                   'time date,' \
                   'title text,' \
                   'url text,' \
                   'endtime date,' \
                   'reserved2 text) DEFAULT CHARSET=utf8;'
    _insertor = u"insert into shanghai(time,title,url,endtime) " \
                " VALUES('{0}','{1}','{2}','{3}');"
    _header = '''
    X-Requested-With: XMLHttpRequest
    X-Prototype-Version: 1.5.1
    Accept: text/javascript, text/html, application/xml, text/xml, */*
    Content-type: application/x-www-form-urlencoded; charset=UTF-8
    useAjaxPrep: true
    Referer: http://www.ccgp-shanghai.gov.cn/news.do?method=purchasePracticeMore&treenum=05&flag=cggg&bFlag=00#title
    Accept-Language: en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3
    Accept-Encoding: gzip, deflate
    User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729)
    Host: www.ccgp-shanghai.gov.cn
    Content-Length: 520
    Connection: Keep-Alive
    Pragma: no-cache
    Cookie: JSESSIONID=2Qf4YHhDwv9P61xrLFDHQ18H2Ng1y1X7wJBZ2kfqgyM1ChLQ1gbh!172237019!355996876
    '''

    _data = 'ec_i=bulletininfotable&bulletininfotable_efn=&bulletininfotable_crd=10&bulletininfotable_p=1&bulletininfotable_s_bulletintitle=&bulletininfotable_s_beginday=&t_query_unitname=&findAjaxZoneAtClient=false&flag=cggg&t_query_flag=1&t_query_year=&bFlag=00&query_sections=00&treenum=05&query_begindaybs=&t_query_bulletintitle=&t_bulletinAgency=&query_begindayes=&method=purchasePracticeMore&method=purchasePracticeMore&bulletininfotable_totalpages=22&bulletininfotable_totalrows=&bulletininfotable_pg=1&bulletininfotable_rd=10'

    def __init__(self):
        print 'Get Data from http://www.ccgp-shanghai.gov.cn/'

    def title(self):
        return self._title

    def getContent(self):
        cn = common.Common()
        ret = []
        try:
            data = cn.postUseRawHeader(self._url,self._header,self._data)
            soup = BeautifulSoup(data, 'html5lib')
            trs = soup.select("#bulletininfotable_table_body tr")
            for tr in trs:
                contents = tr.contents
                title = contents[3].text.strip()
                id = contents[3].a['value']
                url = self._baseurl.format(id)
                times = contents[5].text
                found = re.findall(r"\d{4}-\d{1,2}-\d{1,2}",times)
                time = found[0]
                endtime = found[1]
                ret.append({'time': time, 'title': title, 'url': url,'endtime':endtime})
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
                sql = self._insertor.format(dat['time'], dat['title'], dat['url'],dat['endtime'])
                mo.runNotQuery(sql)
        except Exception as e:
            ret = str(e)
        return ret


if __name__ == '__main__':
    sh = ShangHai()
    ret = sh.getContent()
    print sh.format(ret)
    sh.save2mysql(ret,"reptiles")