#!/usr/bin/env python
# -*- coding: utf-8 -*-

import common
from bs4 import BeautifulSoup
import mysqlop


class AnHui():
    _url = 'www.ccgp-anhui.gov.cn'
    _baseurl = 'http://www.ccgp-anhui.gov.cn/'
    _posturl = '/mhxt/MhxtSearchBulletinController.zc?method=bulletinChannelRightDown'
    _title = u'安徽省政府采购'
    _createtable = 'create table if not exists anhui(' \
                   'id int not null PRIMARY  KEY auto_increment,' \
                   'time date,' \
                   'title text,' \
                   'url text,' \
                   'reserved1 int,' \
                   'reserved2 text) DEFAULT CHARSET=utf8;'
    _insertor = u"insert into anhui(time,title,url) " \
                " VALUES('{0}','{1}','{2}');"
    _header = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'Accept': 'text/html, */*; q=0.01',
               'X-Requested-With': 'XMLHttpRequest',
               'Referer': 'http://www.ccgp-anhui.gov.cn/',
               'Accept-Language': 'zh-Hans-CN,zh-Hans;q=0.8,en-US;q=0.5,en;q=0.3',
               'Accept-Encoding': 'gzip, deflate',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
               'Content-Length': '145',
               'Host': 'www.ccgp-anhui.gov.cn',
               'Connection': 'Keep-Alive',
               'Pragma': 'no-cache'}
    _para = {'channelCode': 'sjcg',
            'bType': '01',
            'areaCode': '340000',
            'type': '00',
            'key': '',
            'bStartDate': '',
            'bEndDate': '',
            'proType': '00',
            'category': '',
            'areaCodeName': '%E7%9C%81%E6%9C%AC%E7%BA%A7',
            'pageNo': '1'}
    # _refer = ''
    # _host = ''
    def __init__(self):
        print 'Get Data from http://www.ccgp-anhui.gov.cn'

    def title(self):
        return self._title

    def getContent(self):
        cn = common.Common()
        ret = []
        try:
            data = cn.post(self._url,self._posturl,self._para,self._header)
            soup = BeautifulSoup(data, 'html5lib')
            lis = soup.select(".column.infoLink.noBox.addState.addStateL.unitWidth_x6 li")
            # print len(lis)
            for li in lis:
                title = li.a['title']
                href = li.a['href']
                time = li.span.text
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
    ah = AnHui()
    ret = ah.getContent()
    print ah.format(ret)
    ah.save2mysql(ret,"reptiles")