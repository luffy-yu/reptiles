#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/13 下午4:20
# @Author  : Luffy
# @Site    : 
# @File    : guangdong.py
# @Software: PyCharm Community Edition

import common
from bs4 import BeautifulSoup
import mysqlop
import re

class GuangDong():
    _url = 'www.gdgpo.gov.cn'
    _baseurl = 'http://www.gdgpo.gov.cn'
    _posturl = '/queryMoreInfoList.do'
    _title = u'广东省政府采购'
    _createtable = 'create table if not exists guangdong(' \
                   'id int not null PRIMARY  KEY auto_increment,' \
                   'time date,' \
                   'title text,' \
                   'url text,' \
                   'reserved1 int,' \
                   'reserved2 text) DEFAULT CHARSET=utf8;'
    _insertor = u"insert into guangdong(time,title,url) " \
                " VALUES('{0}','{1}','{2}');"

    _header = {'Host': 'www.gdgpo.gov.cn',
               'Connection': 'keep-alive',
               'Content-Length': '235',
               'Cache-Control': 'max-age=0',
               'Origin': 'http://www.gdgpo.gov.cn',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Referer': 'http://www.gdgpo.gov.cn/queryMoreInfoList.do',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.8'}
    _para = {'stockTypes': '',
             'channelCode': '000501',
             'regionIds': '',
             'sitewebName': u'广东省',
             'sitewebId': '4028889705bebb510105bec068b00003',
             'title': '',
             'stockNum': '',
             'purchaserOrgName': '',
             'issueOrgan': '',
             'performOrgName': '',
             'stockIndexName': '',
             'operateDateFrom': '',
             'operateDateTo': ''}
    # _refer = ''
    # _host = ''
    def __init__(self):
        print 'Get Data from http://www.gdgpo.gov.cn'

    def title(self):
        return self._title

    def getContent(self):
        cn = common.Common()
        ret = []
        try:
            data = cn.post(self._url,self._posturl,self._para,self._header)
            soup = BeautifulSoup(data, 'html5lib')
            lis = soup.select(".m_m_c_list li")
            for li in lis:
                time = li.em.text
                time = re.search(r"\d{4}-\d{1,2}-\d{1,2}",time).group(0)
                for ch in li.children:
                    if ch.name == 'a':
                        href = ch['href']
                        title = ch['title']
                        url = self._baseurl + href
                        # print time,title,url
                        ret.append({'time': time, 'title': title, 'url': url})
                        break
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
    gd = GuangDong()
    ret =gd.getContent()
    print  gd.format(ret)
    gd.save2mysql(ret,"reptiles")