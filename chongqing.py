#!/usr/bin/env python
# -*- coding: utf-8 -*-

import common
from bs4 import BeautifulSoup
import mysqlop
import re


class ChongQing():
    _url = 'https://www.cqgp.gov.cn/gwebsite/api/v1/notices/stable?' \
           'pi=1&projectPurchaseWay=100&ps=20&' \
           'timestamp={0}&' \
           'type=100,200,201,202,203,204,205,206,207,309,400,401,402,3091,4001' \
           '&zone=130117562645086249'
    _baseurl = 'https://www.cqgp.gov.cn/notices/detail/'
    _title = u'重庆市政府采购'
    _createtable = 'create table if not exists chongqing(' \
                   'id int not null PRIMARY  KEY auto_increment,' \
                   'time date,' \
                   'title text,' \
                   'url text,' \
                   'begintime datetime,' \
                   'endtime datetime) DEFAULT CHARSET=utf8;'
    _insertor = u"insert into chongqing(time,title,url,begintime,endtime) " \
                " VALUES('{0}','{1}','{2}','{3}','{4}');"

    # _refer = ''
    # _host = ''
    def __init__(self):
        print 'Get Data from http://www.cqgp.gov.cn'

    def title(self):
        return self._title

    def getContent(self):
        cn = common.Common()
        ret = []
        try:
            self._url = self._url.format(cn.makeUTCTime())
            data = cn.getHTTPS(self._url)
            dics = eval(data)
            notices = dics['notices']
            for notice in notices:
                title = notice['title']
                issueTime = notice['issueTime']
                time = re.search(r"\d{4}-\d{1,2}-\d{1,2}",issueTime).group(0)
                begintime = notice['bidBeginTime']
                endtime = notice['bidEndTime']
                id = notice['id']
                url = self._baseurl + id
                # begintime = re.search(r"\d{4}-\d{1,2}-\d{1,2}",bidBeginTime).group(0)
                # endtime = re.search(r"\d{4}-\d{1,2}-\d{1,2}",bidEndTime).group(0)
                ret.append({'time': time, 'title': title, 'url': url,'begintime':begintime,'endtime':endtime})
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
                sql = self._insertor.format(dat['time'], dat['title'], dat['url'],dat['begintime'],dat['endtime'])
                mo.runNotQuery(sql)
        except Exception as e:
            ret = str(e)
        return ret


if __name__ == '__main__':
    cq = ChongQing()
    ret = cq.getContent()
    print cq.format(ret)
    cq.save2mysql(ret,"reptiles")