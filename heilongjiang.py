#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/13 下午3:11
# @Author  : Luffy
# @Site    : 
# @File    : heilongjiang.py
# @Software: PyCharm Community Edition

import common
from bs4 import BeautifulSoup
import mysqlop
import re

class HeiLongJiang():
    _url = 'http://www.hljcg.gov.cn/xwzs!queryXwxxqx.action?lbbh=4'
    _baseurl = 'http://www.hljcg.gov.cn'
    _cookieurl = 'http://www.hljcg.gov.cn/xwzs!home.action'
    _title = u'黑龙江省政府采购'
    _createtable = 'create table if not exists heilongjiang(' \
                   'id int not null PRIMARY  KEY auto_increment,' \
                   'time date,' \
                   'title text,' \
                   'url text,' \
                   'reserved1 int,' \
                   'reserved2 text) DEFAULT CHARSET=utf8;'
    _insertor = u"insert into heilongjiang(time,title,url) " \
                " VALUES('{0}','{1}','{2}');"

    _header = {'Host': 'www.hljcg.gov.cn',
               'Connection': 'keep-alive',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Referer': 'http://www.hljcg.gov.cn/xwzs!index.action',
               'Accept-Encoding': 'gzip, deflate, sdch',
               'Accept-Language': 'zh-CN,zh;q=0.8',
               }
    _cookie = {'JSESSIONID': 'Fn1CYHgBPZsTNPxc1B3RK8ybp06P82tvrTYckCfG5GFmkbnjnNRJ!664279253!-70105479'}
    # _refer = ''
    # _host = ''
    def __init__(self):
        print 'Get Data from http://www.hljcg.gov.cn'

    def title(self):
        return self._title

    def getContent(self):
        cn = common.Common()
        ret = []
        try:
            # jid = cn.getCookie(self._cookieurl,'JSESSIONID')
            # self._cookie['JSESSIONID'] = jid
            html = cn.getHtmlUseCookies(self._url,self._cookie,self._header)
            soup = BeautifulSoup(html, 'html5lib')
            divs = soup.select(".yahoo div")
            for div in divs:
                title = div.contents[1].text
                time = div.contents[3].text
                href = re.search(r"'.+'",div.a['onclick']).group(0)
                url = self._baseurl + eval(href)
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
    hlj = HeiLongJiang()
    ret = hlj.getContent()
    print hlj.format(ret)
    hlj.save2mysql(ret,"reptiles")