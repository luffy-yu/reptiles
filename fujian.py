#!/usr/bin/env python
# -*- coding: utf-8 -*-

import common
from bs4 import BeautifulSoup
import mysqlop

class FuJian():
    _url = 'http://cz.fjzfcg.gov.cn/notice/noticelist/'
    _baseurl = 'http://cz.fjzfcg.gov.cn'
    _posturl = '/notice/noticelist/'
    _title = u'福建省政府采购'
    _createtable = 'create table if not exists fujian(' \
                   'id int not null PRIMARY  KEY auto_increment,' \
                   'time date,' \
                   'title text,' \
                   'url text,' \
                   'reserved1 int,' \
                   'reserved2 text) DEFAULT CHARSET=utf8;'
    _insertor = u"insert into fujian(time,title,url) " \
                " VALUES('{0}','{1}','{2}');"

    _header = '''
    Accept: image/gif, image/jpeg, image/pjpeg, application/x-ms-application, application/xaml+xml, application/x-ms-xbap, */*
    Referer: http://cz.fjzfcg.gov.cn/notice/noticelist/
    Accept-Language: en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3
    User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729)
    Content-Type: application/x-www-form-urlencoded
    Accept-Encoding: gzip, deflate
    Content-Length: 197
    Host: cz.fjzfcg.gov.cn
    Connection: Keep-Alive
    Pragma: no-cache
    Cookie: csrftoken=eSP5HfGdeXNRiN2GNRfyXtZYAjNjIXou
    '''

    _data = 'csrfmiddlewaretoken=eSP5HfGdeXNRiN2GNRfyXtZYAjNjIXou&zone_code=350000&notice_type=200000001&gpmethod=100005001&title=&project_no=&croporgan_name=&agency_name=&purchase_item_name=&fromtime=&endtime='
    # _refer = ''
    # _host = ''
    def __init__(self):
        print 'Get Data from http://cz.fjzfcg.gov.cn'

    def title(self):
        return self._title

    def getContent(self):
        cn = common.Common()
        ret = []
        try:
            data = cn.postUseRawHeader(self._url,self._header,self._data)
            html = cn.ungzipData(data)
            soup = BeautifulSoup(html, 'html5lib')
            lis = soup.select(".pag_box20.clearfix li")
            for li in lis:
                href = li.a['href']
                title = li.a.text.strip()
                time = li.span.text
                url = self._baseurl + href
                # print time,title,url
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
    fj = FuJian()
    ret = fj.getContent()
    print fj.format(ret)
    fj.save2mysql(ret,"reptiles")