#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/10 下午1:55
# @Author  : Luffy
# @Site    : 
# @File    : common.py
# @Software: PyCharm Community Edition

'''
公用模块
'''
__all__ =['Common','getHtml','getHtmlAsBrowser']

import urllib2
import chardet
import urllib
import requests
import httplib
from time import *
import datetime

class Common():
    '''
    公用模块
    '''
    def __int__(self):
        print 'Common module'
    def getHtml(self,url):
        '''
        使用content属性可以保证中文不乱码，text属性会使中文乱码
        :param url: 网页链接
        :return: 网页内容
        '''
        # return requests.get(url).content#处理江西省的政府采购时会乱码，采用下面的方法
        ###检测编码方式1--结果不正确
        ## import requests
        ## resp = requests.get(url)
        ## print resp.encoding
        ## print resp.text.encode(resp.encoding).decode('utf-8')
        ###检测编码方式1--结果不正确
        ###检测编码方式2
        ## import chardet
        ## import urllib
        ## data = urllib.urlopen(url).read()
        ## code = chardet.detect(data)['encoding']
        ###检测编码方式2
        # print resp.text.encode('GB18030').decode('GB2312')
        # 使用方法2检测编码，如果是GB2312的编码使用GB18030编码，然后GB2312解码
        data = urllib.urlopen(url).read()
        code = chardet.detect(data)['encoding']
        if str(code).upper() == "GB2312":
            resp = requests.get(url)
            return resp.content.decode('GBK')
            # return resp.text.encode('GB18030').decode('GB2312')
        else:
            return data.encode(code).decode('utf-8')

    def getHtmlAsBrowser(self,url,refer = None,host = None,timeout = 1000):
        '''
        伪装浏览器获取网页内容
        :param url:网页链接
        :param refer:网页引用
        :param timeout:超时时间
        :return:网页内容
        '''
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Referer': refer,  # 注意如果依然不能抓取的话，这里可以设置抓取网站的host
            'Host':host
            }
        req = urllib2.Request(url, None, header)
        resp = urllib2.urlopen(req, None, timeout)
        html = resp.read()
        resp.close()
        return html

    def getHtmlAsBrowser2(self,url,header,timeout = 1000):
        req = urllib2.Request(url, None, header)
        resp = urllib2.urlopen(req, None, timeout)
        html = resp.read()
        resp.close()
        return html

    def getHtmlUseCookies(self,url,cookies,header):
        req = requests.get(url,cookies = cookies,headers = header)
        # print req.status_code
        html = req.content
        req.close()
        return html

    def post(self,host,url,para,header):
        conn = httplib.HTTPConnection(host)
        params = urllib.urlencode(para)
        conn.request('POST',url,params,header)
        resp = conn.getresponse()
        #print resp.status
        content = resp.read()
        # 如果数据是采用gzip的方式压缩的
        if resp.getheader('content-encoding') == 'gzip':
            import gzip
            import StringIO
            data = StringIO.StringIO(content)
            gz = gzip.GzipFile(fileobj=data)
            content = gz.read()
            gz.close()
        resp.close()
        return content
    def get(self,host,url,para,header):
        conn = httplib.HTTPConnection(host)
        params = urllib.urlencode(para)
        conn.request('GET',url,params,header)
        resp = conn.getresponse()
        content = resp.read()
        # # 如果数据是采用gzip的方式压缩的
        # if resp.getheader('content-encoding') == 'gzip':
        #     import gzip
        #     import StringIO
        #     data = StringIO.StringIO(content)
        #     gz = gzip.GzipFile(fileobj=data)
        #     content = gz.read()
        #     gz.close()
        resp.close()
        return content

    def makeUTCTime(self):
        t = (mktime(datetime.datetime.utcnow().timetuple()) + 3600 * 8) * 1000
        return "%d" % t
    def getHTTPS(self,url):
        #以下三行禁用警告
        from requests.packages.urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        # requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)

        resp = requests.get(url, verify=False)
        return resp.text.encode(resp.encoding).decode('utf-8')

    def postUseRawHeader(self,url,headers,data):
        import urllib2
        headers = dict([[field.strip() for field in pair.split(':', 1)] for pair in headers.strip().split('\n')])
        req = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(req)
        html = response.read()
        response.close()
        return html

    def formatRawHeader(self,headers):
        return dict([[field.strip() for field in pair.split(':', 1)] for pair in headers.strip().split('\n')])

    def ungzipData(self,html):
        import gzip
        import StringIO
        data = StringIO.StringIO(html)
        gz = gzip.GzipFile(fileobj=data)
        ret = gz.read()
        gz.close()
        return ret

    def getCookie(self,url,key):
        import cookielib
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
        resp = urllib2.urlopen(url)#or resp = opener.open(url)
        ret = None
        for cookie in cj:
            if cookie.name == key:
                ret = cookie.value
                break
        return ret

if __name__ == '__main__':
    # import common
    # help(common)
    cn = Common()
    print cn.getCookie('http://www.hljcg.gov.cn/xwzs!home.action','JSESSIONID')