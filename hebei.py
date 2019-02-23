#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/13 下午2:26
# @Author  : Luffy
# @Site    : 
# @File    : hebei.py
# @Software: PyCharm Community Edition

import common
from bs4 import BeautifulSoup
import mysqlop
import re

class HeBei():
    _url = 'www.ccgp-hebei.gov.cn'
    _baseurl = 'http://www.ccgp-hebei.gov.cn'
    _posturl = '/zfcg/web/getBidingList_1.html'
    _title = u'河北省政府采购'
    _createtable = 'create table if not exists hebei(' \
                   'id int not null PRIMARY  KEY auto_increment,' \
                   'time date,' \
                   'title text,' \
                   'url text,' \
                   'reserved1 int,' \
                   'reserved2 text) DEFAULT CHARSET=utf8;'
    _insertor = u"insert into hebei(time,title,url) " \
                " VALUES('{0}','{1}','{2}');"

    _header = {'Host': 'www.ccgp-hebei.gov.cn',
               'Connection': 'keep-alive',
               'Content-Length': '62',
               'Cache-Control': 'max-age=0',
               'Origin': 'http://www.ccgp-hebei.gov.cn',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Referer': 'http://www.ccgp-hebei.gov.cn/zfcg/web/getBidingList_1.html',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.8'}

    _para = {'citycode': '',
             'cityname': '',
             'biddingannc': '',
             'levelFlag': '',
             'areaCode': '130000000'}
    # _refer = ''
    # _host = ''
    def __init__(self):
        print 'Get Data from http://www.ccgp-hebei.gov.cn'

    def title(self):
        return self._title

    def getContent(self):
        cn = common.Common()
        ret = []
        try:
            data = cn.post(self._url,self._posturl,self._para,self._header)
            # print data
            soup = BeautifulSoup(data, 'html5lib')
            trs = soup.select("#moredingannctable tbody tr")
            # print len(trs)
            for tr in trs:
                if tr.has_attr('onclick'):
                    # print tr.attrs['onclick']
                    watchContent = tr.attrs['onclick']
                    match = re.findall(r"\d+",watchContent)
                    # [u'80244', u'1']
                    flag = match[1]
                    fid = match[0]
                    href = "/zfcg/"+flag+"/bidingAnncDetail_"+fid+".html"
                    url = self._baseurl + href
                a = tr.a
                span = tr.span
                if a is not None:
                    title = a.text
                if span is not None:
                    time = span.text
                    # print time,title,url
                    ret.append({'time': time, 'title': title, 'url': url})
                    # break
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
    hb = HeBei()
    ret = hb.getContent()
    print hb.format(ret)
    hb.save2mysql(ret,"reptiles")