#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/10 下午2:01
# @Author  : Luffy
# @Site    : 
# @File    : sendemail.py
# @Software: PyCharm Community Edition

'''
发送邮件模块
'''

__all__ = ['SendEmail','addReceiver','setReceiver','send']
import smtplib
from email.mime.text import MIMEText

class SendEmail():
    '''
    发送邮件模块
    '''
    _tolist = []
    _host = "smtp.xxxxx.com"
    _user = "xxxx"
    _pass = "xxxxxxxxxxxxxxx"
    _postfix = "xxxxx.xxxx"

    def __int__(self):
        print "SendEmail module"
    def addReceiver(self,user):
        '''
        添加收件人
        :param user:收件人
        :return:None
        '''
        self._tolist.append(user)
    def setReceiver(self,list):
        '''
        设置收件人
        :param list:收件人列表
        :return:None
        '''
        self._tolist = list
    def send(self,title,content,type='plain'):
        '''
        发送邮件
        :param title:标题
        :param content:内容
        :param type:类型，'plain' or 'html'
        :return:成功返回True，失败返回False
        '''
        if len(self._tolist) < 1:
            print "Undefined receiver."
            return False
        me = "xxxxx" + "<" + self._user + "@" + self._postfix + ">"
        if type == 'plain':
            msg = MIMEText(content,_subtype='plain',_charset='utf-8')
        elif type == 'html':
            msg = MIMEText(content,_subtype='html',_charset='utf-8')
        else:
            print 'Unsupported type.'
            return False
        msg['Subject'] = title
        msg['From'] = me
        msg['To'] = ",".join(self._tolist)
        try:
            server = smtplib.SMTP()
            server.connect(self._host)
            server.login(self._user,self._pass)
            server.sendmail(me,self._tolist,msg.as_string())
            server.close()
            print 'Send E-mail succeed.'
            return True
        except Exception as e:
            print str(e)
            return False

if __name__ == '__main__':
    # se = SendEmail()
    # se.addReceiver("xxxxx@xxxxx.com")
    # se.addReceiver("xxxxx@xxxxx.com")
    # se.send("Test","Haha")
    import sendemail
    help(sendemail)