#!/usr/bin/env python
# -*- coding: utf-8 -*-

import common
from bs4 import BeautifulSoup
import mysqlop
import re

class GuangXi():
    _url = 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-shengji_cggg/param_bulletin/20/page_1.html'
    _baseurl = 'http://www.ccgp-guangxi.gov.cn'
    _title = u'广西政府采购'
    _createtable = 'create table if not exists guangxi(' \
                   'id int not null PRIMARY  KEY auto_increment,' \
                   'time date,' \
                   'title text,' \
                   'url text,' \
                   'reserved1 int,' \
                   'reserved2 text) DEFAULT CHARSET=utf8;'
    _insertor = u"insert into guangxi(time,title,url) " \
                " VALUES('{0}','{1}','{2}');"

    _header = {'Host': 'www.ccgp-guangxi.gov.cn',
               'Connection': 'keep-alive',
               'Cache-Control': 'max-age=0',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, sdch',
               'Accept-Language': 'zh-CN,zh;q=0.8'}

    _cookie = {'JSESSIONID': 'F7712CE86D3991C06BC5B5BC90FBFA6E'}
    # _refer = ''
    # _host = ''
    def __init__(self):
        print 'Get Data from http://www.ccgp-guangxi.gov.cn'

    def title(self):
        return self._title

    def getContent(self):
        cn = common.Common()
        ret = []
        try:
            # html = cn.getHtml(self._url)#[Errno socket error] [Errno 61] Connection refused
            html = cn.getHtmlUseCookies(self._url,self._cookie,self._header)
            soup = BeautifulSoup(html, 'html5lib')
            lis = soup.select(".column.infoLink.noBox.unitWidth_x6 li")
            for li in lis:
                href = li.a['href']
                title = li.a['title']#包含有竞争性谈判内容
                time =re.search(r"\d{4}-\d{1,2}-\d{1,2}",li.text).group(0)#可以有更优的实现
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
    gx = GuangXi()
    ret = gx.getContent()
    print gx.format(ret)
    gx.save2mysql(ret,"reptiles")