#!/usr/bin/env python
# -*- coding: utf-8 -*-

import common
from bs4 import BeautifulSoup
import mysqlop
import re


class Xinjiang():
    _url = 'http://zfcg.xjcz.gov.cn/djl/cmsPublishAction.do?method=selectCmsInfoPublishList&channelId=15'
    _baseurl = 'http://zfcg.xjcz.gov.cn'
    _title = u'新疆政府采购'
    _createtable = 'create table if not exists xinjiang(' \
                   'id int not null PRIMARY  KEY auto_increment,' \
                   'time date,' \
                   'title text,' \
                   'url text,' \
                   'reserved1 int,' \
                   'reserved2 text) DEFAULT CHARSET=utf8;'
    _insertor = u"insert into xinjiang(time,title,url) " \
                " VALUES('{0}','{1}','{2}');"

    # _refer = ''
    # _host = ''
    def __init__(self):
        print 'Get Data from http://zfcg.xjcz.gov.cn'

    def title(self):
        return self._title

    def getContent(self):
        cn = common.Common()
        ret = []
        try:
            html = cn.getHtml(self._url)
            soup = BeautifulSoup(html, 'html5lib')
            # print html
            divs = soup.select(".left.layout2_list_row2")
            for div in divs:
                time = re.search(r"\d{4}-\d{1,2}-\d{1,2}", div.text).group(0)
                href = div.a['href']
                title = div.a.text
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
    xj = Xinjiang()
    ret = xj.getContent()
    print xj.format(ret)
    xj.save2mysql(ret,"reptiles")