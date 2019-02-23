#!/usr/bin/env python
# -*- coding: utf-8 -*-

import common
# from bs4 import BeautifulSoup
import mysqlop

class HuNan():
    _url = 'www.ccgp-hunan.gov.cn'
    _posturl = '/mvc/getNoticeList4Web.do'
    _baseurl = 'http://www.ccgp-hunan.gov.cn/page/notice/notice.jsp?noticeId='
    _title = u'湖南省政府采购'
    _createtable = 'create table if not exists hunan(' \
                   'id int not null PRIMARY  KEY auto_increment,' \
                   'time date,' \
                   'title text,' \
                   'url text,' \
                   'reserved1 int,' \
                   'reserved2 text) DEFAULT CHARSET=utf8;'
    _insertor = u"insert into hunan(time,title,url) " \
                " VALUES('{0}','{1}','{2}');"

    #'pageSize': '18'这个是默认参数，可以修改
    _para = {'nType':'prcmNotices',
               'pType': '01',
               'prcmPrjName': '',
               'prcmItemCode':'',
               'prcmOrgName': '',
               'startDate': '',
               'endDate': '',
               'prcmPlanNo': '',
               'page': '1',
               'pageSize': '18'}
    _header = {"Host": "www.ccgp-hunan.gov.cn",
                "Connection": "keep-alive",
                "Content-Length": "117",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Origin": "http://www.ccgp-hunan.gov.cn",
                "X-Requested-With": "XMLHttpRequest",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Referer": "http://www.ccgp-hunan.gov.cn/page/notice/more.jsp?prcmMode=01",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.8"}#,
                #"Cookie":"JSESSIONID = k4wQYGFJltpksqzGQhTWyFWpm4SCmWwgtGtFLNFfFSl1zlWtkHS7!676160331!NONE"};
    # _refer = ''
    # _host = ''
    def __init__(self):
        print 'Get Data from http://www.ccgp-hunan.gov.cn'

    def title(self):
        return self._title

    def getContent(self):
        cn = common.Common()
        ret = []
        try:
            data = cn.post(self._url,self._posturl,self._para,self._header)
            # print data
            dics =  eval(data.replace("null","'null'"))
            for dic in dics["rows"]:
                title = dic["NOTICE_TITLE"]
                time = dic["NEWWORK_DATE"]
                id = dic["NOTICE_ID"]
                url = self._baseurl + str(id)
                # print title,time,url
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
    hn = HuNan()
    ret = hn.getContent()
    print hn.format(ret)
    hn.save2mysql(ret,"reptiles")