#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/10 下午2:48
# @Author  : Luffy
# @Site    : 
# @File    : main.py
# @Software: PyCharm Community Edition

'''
主程序
'''
import sendemail
import shxga
import shanxi
import shaanxi
import bgpc
import tjgp
import shandong
import hngp
import jiangsu
import jiangxi
import zhejiang
import hunan
import hubei
import hebei
import jilin
import liaoning
import guangdong
import hainan
import neimenggu
import gansu
import qinghai
import ningxia
import xinjiang
import xizang
import sichuan
import guangxi
import yunnan
import anhui
import guizhou
import chongqing
import heilongjiang
import shanghai
import fujian
import bjcz

def spyShxga(reclist):
    '''
    爬取陕西省公安厅招标信息，并发送邮件
    :param reclist:收件人列表
    :return:None
    '''
    se = sendemail.SendEmail()
    se.setReceiver(reclist)
    sa = shxga.Shxga()
    ret = sa.getContent()
    content = sa.format(ret)
    se.send(sa.title(),content,type='html')

def spyShanxi(reclist):
    se = sendemail.SendEmail()
    se.setReceiver(reclist)
    sx = shanxi.ShanXi()
    ret = sx.getContent()
    content = sx.format(ret)
    se.send(sx.title(),content,type='html')

def spyShaanxi(reclist):
    se = sendemail.SendEmail()
    se.setReceiver(reclist)
    sx = shaanxi.ShaanXi()
    ret = sx.getContent()
    content = sx.format(ret)
    se.send(sx.title(),content,type='html')

def spyBgpc(reclist):
    se = sendemail.SendEmail()
    se.setReceiver(reclist)
    bg = bgpc.Bgpc()
    ret = bg.getContent()
    content = bg.format(ret)
    se.send(bg.title(),content,type='html')

def spyTjgp(reclist):
    se = sendemail.SendEmail()
    se.setReceiver(reclist)
    tj = tjgp.Tjgp()
    ret = tj.getContent()
    content = tj.format(ret)
    se.send(tj.title(), content, type='html')

def spyShanDong(reclist):
    se = sendemail.SendEmail()
    se.setReceiver(reclist)
    sd = shandong.ShanDong()
    ret = sd.getContent()
    content = sd.format(ret)
    se.send(sd.title(), content, type='html')
def spyHngp(reclist):
    se = sendemail.SendEmail()
    se.setReceiver(reclist)
    hn = hngp.Hngp()
    ret = hn.getContent()
    content = hn.format(ret)
    se.send(hn.title(), content, type='html')

def spyJiangSu(reclist):
    se = sendemail.SendEmail()
    se.setReceiver(reclist)
    js = jiangsu.JiangSu()
    ret = js.getContent()
    content = js.format(ret)
    se.send(js.title(), content, type='html')

def spyJiangXi(reclist):
    se = sendemail.SendEmail()
    se.setReceiver(reclist)
    jx = jiangxi.JiangXi()
    ret = jx.getContent()
    content = jx.format(ret)
    se.send(jx.title(), content, type='html')

def spyZheJiang(reclist):
    se = sendemail.SendEmail()
    se.setReceiver(reclist)
    zj = zhejiang.ZheJiang()
    ret = zj.getContent()
    content = zj.format(ret)
    se.send(zj.title(), content, type='html')

def spyHuNan(reclist):
    se = sendemail.SendEmail()
    se.setReceiver(reclist)
    hn = hunan.HuNan()
    ret = hn.getContent()
    content = hn.format(ret)
    se.send(hn.title(), content, type='html')

def spyHuBei(reclist):
    se = sendemail.SendEmail()
    se.setReceiver(reclist)
    hb = hubei.HuBei()
    ret = hb.getContent()
    content = hb.format(ret)
    se.send(hb.title(), content, type='html')

def spyHeBei(reclist):
    se = sendemail.SendEmail()
    se.setReceiver(reclist)
    hb = hebei.HeBei()
    ret = hb.getContent()
    content = hb.format(ret)
    se.send(hb.title(), content, type='html')

def spyJiLin(reclist):
    se = sendemail.SendEmail()
    se.setReceiver(reclist)
    jn = jilin.JiLin()
    ret = jn.getContent()
    content = jn.format(ret)
    se.send(jn.title(), content, type='html')

def spyLiaoNing(reclist):
    se = sendemail.SendEmail()
    se.setReceiver(reclist)
    ln = liaoning.LiaoNing()
    ret = ln.getContent()
    content = ln.format(ret)
    se.send(ln.title(), content, type='html')

def spyGuangDong(reclist):
    se = sendemail.SendEmail()
    se.setReceiver(reclist)
    gd = guangdong.GuangDong()
    ret = gd.getContent()
    content = gd.format(ret)
    se.send(gd.title(), content, type='html')

def spyHaiNan(reclist):
    se = sendemail.SendEmail()
    se.setReceiver(reclist)
    hn = hainan.HaiNan()
    ret = hn.getContent()
    content = hn.format(ret)
    se.send(hn.title(), content, type='html')

def spyNeiMengGu(reclist):
    se = sendemail.SendEmail()
    se.setReceiver(reclist)
    nmg = neimenggu.NeiMengGu()
    ret = nmg.getContent()
    content = nmg.format(ret)
    se.send(nmg.title(), content, type='html')

def spyGanSu(reclist):
    se = sendemail.SendEmail()
    se.setReceiver(reclist)
    gs = gansu.GanSu()
    ret = gs.getContent()
    content = gs.format(ret)
    se.send(gs.title(), content, type='html')

def spyQingHai(reclist):
    se = sendemail.SendEmail()
    se.setReceiver(reclist)
    qh = qinghai.QingHai()
    ret = qh.getContent()
    content = qh.format(ret)
    se.send(qh.title(), content, type='html')

def spyNingXia(reclist):
    se = sendemail.SendEmail()
    se.setReceiver(reclist)
    nx = ningxia.NingXia()
    ret = nx.getContent()
    content = nx.format(ret)
    se.send(nx.title(), content, type='html')

def spyXinJiang(reclist):
    se = sendemail.SendEmail()
    se.setReceiver(reclist)
    xj = xinjiang.Xinjiang()
    ret = xj.getContent()
    content = xj.format(ret)
    se.send(xj.title(), content, type='html')

def spyXiZang(reclist):
    se = sendemail.SendEmail()
    se.setReceiver(reclist)
    xz = xizang.XiZang()
    ret = xz.getContent()
    content = xz.format(ret)
    se.send(xz.title(), content, type='html')

def spySiChuan(reclist):
    se = sendemail.SendEmail()
    se.setReceiver(reclist)
    sc = sichuan.SiChuan()
    ret = sc.getContent()
    content = sc.format(ret)
    se.send(sc.title(), content, type='html')

def spyGuangXi(reclist):
    se = sendemail.SendEmail()
    se.setReceiver(reclist)
    gx = guangxi.GuangXi()
    ret = gx.getContent()
    content = gx.format(ret)
    se.send(gx.title(), content, type='html')

def spyYunNan(reclist):
    se = sendemail.SendEmail()
    se.setReceiver(reclist)
    yn = yunnan.YunNan()
    ret = yn.getContent()
    content = yn.format(ret)
    se.send(yn.title(), content, type='html')

def spyAnHui(reclist):
    se = sendemail.SendEmail()
    se.setReceiver(reclist)
    ah = anhui.AnHui()
    ret = ah.getContent()
    content = ah.format(ret)
    se.send(ah.title(), content, type='html')

def spyGuiZhou(reclist):
    se = sendemail.SendEmail()
    se.setReceiver(reclist)
    gz = guizhou.GuiZhou()
    ret = gz.getContent()
    content = gz.format(ret)
    se.send(gz.title(), content, type='html')

def spyChongQing(reclist):
    se = sendemail.SendEmail()
    se.setReceiver(reclist)
    cq = chongqing.ChongQing()
    ret = cq.getContent()
    content = cq.format(ret)
    se.send(cq.title(), content, type='html')

def spyHeiLongJiang(reclist):
    se = sendemail.SendEmail()
    se.setReceiver(reclist)
    hlj = heilongjiang.HeiLongJiang()
    ret = hlj.getContent()
    content = hlj.format(ret)
    se.send(hlj.title(), content, type='html')

def spyShangHai(reclist):
    se = sendemail.SendEmail()
    se.setReceiver(reclist)
    sh = shanghai.ShangHai()
    ret = sh.getContent()
    content = sh.format(ret)
    se.send(sh.title(), content, type='html')

def spyFuJian(reclist):
    se = sendemail.SendEmail()
    se.setReceiver(reclist)
    fj = fujian.FuJian()
    ret = fj.getContent()
    content = fj.format(ret)
    se.send(fj.title(), content, type='html')

# 北京财政局
def spyBjcz(reclist):
    se = sendemail.SendEmail()
    se.setReceiver(reclist)
    bj = bjcz.Bjcz()
    ret = bj.getContent()
    content = bj.format(ret)
    se.send(bj.title(), content, type='html')

if __name__ == '__main__':
    reclist = ['xxx@xxxx.com']
    spyShxga(reclist)
    spyShanxi(reclist)
    spyShaanxi(reclist)
    spyBgpc(reclist)
    spyTjgp(reclist)
    spyShanDong(reclist)#empty
    spyHngp(reclist)
    spyJiangSu(reclist)
    spyJiangXi(reclist)#time out
    spyZheJiang(reclist)
    spyHuNan(reclist)
    spyHuBei(reclist)
    spyHeBei(reclist)#empty
    spyJiLin(reclist)
    spyLiaoNing(reclist)
    spyGuangDong(reclist)
    spyHaiNan(reclist)
    spyNeiMengGu(reclist)
    spyGanSu(reclist)
    spyQingHai(reclist)
    spyNingXia(reclist)
    spyXinJiang(reclist)
    spyXiZang(reclist)
    spySiChuan(reclist)
    spyGuangXi(reclist)
    spyYunNan(reclist)
    spyAnHui(reclist)
    spyGuiZhou(reclist)
    spyChongQing(reclist)#[SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert handshake failure (_ssl.c:661) pip install requests[security]
    spyHeiLongJiang(reclist)#('Connection aborted.', BadStatusLine("''",))
    spyShangHai(reclist)
    spyFuJian(reclist)
    spyBjcz(reclist)