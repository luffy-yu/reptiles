#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/13 下午3:37
# @Author  : Luffy
# @Site    : 
# @File    : liaoning.py
# @Software: PyCharm Community Edition

import common
from bs4 import BeautifulSoup
import mysqlop
import re


class LiaoNing():
    _url = 'www.ccgp-liaoning.gov.cn'
    _baseurl = 'http://www.ccgp-liaoning.gov.cn/bulletin.do?method=showbulletin&bulletin_id='
    _posturl = '/bulletininfo.do?method=bdetail'
    _title = u'辽宁省政府采购'
    _createtable = 'create table if not exists liaoning(' \
                   'id int not null PRIMARY  KEY auto_increment,' \
                   'time date,' \
                   'title text,' \
                   'url text,' \
                   'endtime date,' \
                   'reserved2 text) DEFAULT CHARSET=utf8;'
    _insertor = u"insert into liaoning(time,title,url,endtime) " \
                " VALUES('{0}','{1}','{2}','{3}');"

    _header = {'X-Requested-With': 'XMLHttpRequest',
               'X-Prototype-Version': '1.5.1',
               'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
               'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'useAjaxPrep': 'true',
               'Referer': 'http://www.ccgp-liaoning.gov.cn/bulletininfo.do?method=bdetail&treenum=05&treenumfalse=',
               'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
               'Accept-Encoding': 'gzip, deflate',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
               'Host': 'www.ccgp-liaoning.gov.cn',
               'Content-Length': '476',
               'Connection': 'Keep-Alive',
               'Pragma': 'no-cache'}
    _para = {'ec_i': 'bulletininfotable',
             'bulletininfotable_efn': '',
             'bulletininfotable_crd': '20',
             'bulletininfotable_p': '1',
             'bulletininfotable_s_bulletintitle': '',
             'bulletininfotable_s_ifwithdraw': '',
             'bulletininfotable_s_beginday': '',
             'treenum': '05',
             'treenumfalse': '',
             'method': 'bdetail',
             'bulletininfotable_totalpages': '1971',
             'bulletininfotable_totalrows': '',
             'bulletininfotable_pg': '1',
             'bulletininfotable_rd': '20',
             't_query_bulletintitle': '',
             'query_begindaybs': '',
             'query_begindayes': '',
             'query_sections': '210000',
             't_query_year': '',
             't_query_flag': '0',
             'findAjaxZoneAtClient': 'false'}
    # _refer = ''
    # _host = ''
    def __init__(self):
        print 'Get Data from http://www.ccgp-liaoning.gov.cn'

    def title(self):
        return self._title

    def getContent(self):
        cn = common.Common()
        ret = []
        try:
            data = cn.post(self._url,self._posturl,self._para,self._header)
            soup = BeautifulSoup(data, 'html5lib')
            trs = soup.select("#bulletininfotable_table_body tr")
            for tr in trs:
                match = re.findall(r"\d{4}-\d{1,2}-\d{1,2}",tr.text)
                time = match[0]
                endtime = match[1]
                a = tr.a
                if a is not None:
                    id = a['value']
                    title = a.text
                    url = self._baseurl + str(id)
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
    ln = LiaoNing()
    ret = ln.getContent()
    print ln.format(ret)
    ln.save2mysql(ret,"reptiles")