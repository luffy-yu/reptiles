#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/13 上午9:46
# @Author  : Luffy
# @Site    : 
# @File    : hubei.py
# @Software: PyCharm Community Edition

import common
from bs4 import BeautifulSoup
import mysqlop
import re


class HuBei():
    _url = 'www.ccgp-hubei.gov.cn'
    _baseurl = 'http://www.ccgp-hubei.gov.cn'
    _title = u'湖北省政府采购'
    _posturl = '/fnoticeAction!listFNoticeInfos_n.action'

    _para = {'rank' : '',
             'queryInfo.curPage':'0',
             'queryInfo.pageSize':'0',
             'queryInfo.TITLE':'',
             'queryInfo.FBRMC':'',
             'queryInfo.GGLX':u'招标公告',
             'queryInfo.CGLX':'',
             'queryInfo.CGFS':u'公开招标',
             'queryInfo.BEGINTIME1':'',
             'queryInfo.ENDTIME1':'',
             'queryInfo.QYBM':'420001',
             'queryInfo.JHHH':''}

    _header = {"Host": "www.ccgp-hubei.gov.cn",
                "Connection": "keep-alive",
                "Content-Length": "280",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Origin": "http://www.ccgp-hubei.gov.cn",
                "X-Requested-With": "XMLHttpRequest",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Referer": "http://www.ccgp-hubei.gov.cn/fnoticeAction!listFNoticeInfos_n.action",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.8"}
    _createtable = 'create table if not exists hubei(' \
                   'id int not null PRIMARY  KEY auto_increment,' \
                   'time date,' \
                   'title text,' \
                   'url text,' \
                   'reserved1 int,' \
                   'reserved2 text) DEFAULT CHARSET=utf8;'
    _insertor = u"insert into hubei(time,title,url) " \
                " VALUES('{0}','{1}','{2}');"

    # _refer = ''
    # _host = ''
    def __init__(self):
        print 'Get Data from http://www.ccgp-hubei.gov.cn'

    def title(self):
        return self._title

    def getContent(self):
        cn = common.Common()
        ret = []
        try:
            data = cn.post(self._url,self._posturl,self._para,self._header)
            soup = BeautifulSoup(data, 'html5lib')
            lis = soup.select(".news_content  ul li")
            for li in lis:
                time = re.search(r"\d{4}-\d{1,2}-\d{1,2}",li.span.text).group(0)
                title = li.a.text.strip()
                href = li.a['href']
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
    hb = HuBei()
    ret = hb.getContent()
    print ret
    hb.save2mysql(ret,"reptiles")
