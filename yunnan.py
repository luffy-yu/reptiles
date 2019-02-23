#!/usr/bin/env python
# -*- coding: utf-8 -*-

import common
from bs4 import BeautifulSoup
import mysqlop


class YunNan():
    _url = 'www.yngp.com'
    _baseurl = 'http://www.yngp.com/bulletin_zz.do?method=showBulletin&bulletin_id='
    _posturl = '/bulletin.do?method=moreListQuery'
    _title = u'云南省政府采购'
    _createtable = 'create table if not exists yunnan(' \
                   'id int not null PRIMARY  KEY auto_increment,' \
                   'time date,' \
                   'title text,' \
                   'url text,' \
                   'reserved1 int,' \
                   'reserved2 text) DEFAULT CHARSET=utf8;'
    _insertor = u"insert into yunnan(time,title,url) " \
                " VALUES('{0}','{1}','{2}');"
    _header = {'Host': 'www.yngp.com',
               'Connection': 'keep-alive',
               'Content-Length': '183',
               'Accept': '*/*',
               'Origin': 'http://www.yngp.com',
               'X-Requested-With': 'XMLHttpRequest',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'Referer': 'http://www.yngp.com/bulletin.do?method=moreList',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.8'}
    #rowCount 默认10
    _para = {'current': '1',
             'rowCount': '10',
             'searchPhrase': '',
             'sign': '1',
             'query_bulletintitle': u'招标',
             'query_startTime': '',
             'query_endTime': '',
             'query_sign': '1',
             'query_codeName': '530000',
             'flag': '1',
             'listSign': '0',
             'districtCode': 'all'}
    # _refer = ''
    # _host = ''
    def __init__(self):
        print 'Get Data from http://www.yngp.com'

    def title(self):
        return self._title

    def getContent(self):
        cn = common.Common()
        ret = []
        try:
            data = cn.post(self._url,self._posturl,self._para,self._header)
            # soup = BeautifulSoup(html, 'html5lib')
            dics = eval(data.replace("null", "'null'").replace("false","'false'"))
            for row in dics['rows']:
                id = row['bulletin_id']
                url = self._baseurl + id
                title = str(row['bulletintitle']).decode('GB2312')
                time = row['beginday']
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
    yn = YunNan()
    ret = yn.getContent()
    print yn.format(ret)
    yn.save2mysql(ret,"reptiles")