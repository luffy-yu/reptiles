#!/usr/bin/env python
# -*- coding: utf-8 -*-

import common
from bs4 import BeautifulSoup
import mysqlop
import re


class GanSu():
    _url = 'http://www.ccgp-gansu.gov.cn/web/doSearch.action?' \
           'op=%271%27&articleSearchInfoVo.title=&articleSearchInfoVo.bidcode=' \
           '&articleSearchInfoVo.proj_name=&articleSearchInfoVo.agentname=' \
           '&articleSearchInfoVo.buyername=&articleSearchInfoVo.division=' \
           '&articleSearchInfoVo.classname=1280501&articleSearchInfoVo.dtype=62' \
           '&articleSearchInfoVo.bidstarttime=&articleSearchInfoVo.bidendtime=&articleSearchInfoVo.tflag=1'
    _baseurl = 'http://www.ccgp-gansu.gov.cn'
    _title = u'甘肃省政府采购'
    # time：发布时间 开标时间：kaibiaotime
    _createtable = 'create table if not exists gansu(' \
                   'id int not null PRIMARY  KEY auto_increment,' \
                   'time date,' \
                   'title text,' \
                   'url text,' \
                   'kaibiaotime date,' \
                   'reserved2 text) DEFAULT CHARSET=utf8;'
    _insertor = u"insert into gansu(time,title,url,kaibiaotime) " \
                " VALUES('{0}','{1}','{2}','{3}');"

    # _refer = ''
    # _host = ''
    def __init__(self):
        print 'Get Data from http://www.ccgp-gansu.gov.cn'

    def title(self):
        return self._title

    def getContent(self):
        cn = common.Common()
        ret = []
        try:
            html = cn.getHtml(self._url)
            soup = BeautifulSoup(html, 'html5lib')
            lis = soup.select(".Expand_SearchSLisi li")
            for li in lis:
                href = li.a['href']
                url = self._baseurl + href
                title = li.a.text
                match = re.findall(r"\d{4}-\d{1,2}-\d{1,2}",li.p.text)
                time = match[1]
                kaibiaotime = match[0]
                # break
                ret.append({'time': time, 'title': title, 'url': url,'kaibiaotime':kaibiaotime})
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
                sql = self._insertor.format(dat['time'], dat['title'], dat['url'],dat['kaibiaotime'])
                mo.runNotQuery(sql)
        except Exception as e:
            ret = str(e)
        return ret


if __name__ == '__main__':
    gs = GanSu()
    ret = gs.getContent()
    print gs.format(ret)
    gs.save2mysql(ret,"reptiles")