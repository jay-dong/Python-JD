 #!/usr/bin/env python
#!coding=utf-8
import urllib
import urllib2
import cookielib
from lxml import etree
import sys
import Cookie
'''
    写的有点乱哈，仅使用玩耍

'''
class loginParam:
    
    def __init__(self):
        url="https://passport.jd.com/uc/login"
        html=urllib2.urlopen(url).read()
        self.selector=etree.HTML(html)
        
    def getToken(self):
        
        return self.selector.xpath("//form[@id='formlogin']/input[@id='token']/@value")
    
    def getUuid(self):
        
        return self.selector.xpath("//form[@id='formlogin']/input[@id='uuid']/@value")
    
    def getLoginType(self):
        
        return self.selector.xpath("//form[@id='formlogin']/input[@id='loginType']/@value")
    
    def getAuthCode(self):
        
        return self.selector.xpath("//form[@id='formlogin']/input[@id='authcode']/@value")
    
    def getPubKey(self):
        
        return self.selector.xpath("//form[@id='formlogin']/input[@id='pubKey']/@value")

    def getSatoken(self):
        
        return self.selector.xpath("//form[@id='formlogin']/input[@id='sa_token']/@value")

        
class JdCookie:
    
    def __init__(self):
        pass

    
    def loginParam(self):
        
        loginInfo=loginParam()
        postData=urllib.urlencode({
            'uuid':loginInfo.getUuid(),
            '_t':loginInfo.getToken(),
            'loginType':loginInfo.getLoginType(),
            'loginname':'15718888884',
            'nloginpwd':'lqd.123456',
            'authcode':loginInfo.getAuthCode(),
            'pubKey':loginInfo.getPubKey(),
            'sa_token':loginInfo.getSatoken(),  
            })
        return postData
    
    def loginSaveCookie(self):

        #设置保存cookie的文件
        filename = 'cookie.txt'
        #声明一个MozillaCookieJar对象来保存cookie，之后写入文件
        cookie = cookielib.MozillaCookieJar(filename)
        #创建cookie处理器
        handler = urllib2.HTTPCookieProcessor(cookie)
        #构建opener
        opener = urllib2.build_opener(handler)
        #创建请求
        res = opener.open('https://passport.jd.com/uc/loginService',self.loginParam())
        #保存cookie到文件
        #ignore_discard的意思是即使cookies将被丢弃也将它保存下来
        #ignore_expires的意思是如果在该文件中cookies已经存在，则覆盖原文件写入
        for item in cookie:
            print 'name:' + item.name + '-value:' + item.value
        
        sys.exit()
        cookie.save(ignore_discard=True,ignore_expires=True)
        
    def getCookie(self):
        #创建一个MozillaCookieJar对象
        cookie = cookielib.MozillaCookieJar()
        #从文件中的读取cookie内容到变量
        cookie.load('cookie.txt',ignore_discard=True,ignore_expires=True)
        #打印cookie内容,证明获取cookie成功
        for item in cookie:
            print 'name:' + item.name + '-value:' + item.value
        #利用获取到的cookie创建一个opener
        handler = urllib2.HTTPCookieProcessor(cookie)
        opener = urllib2.build_opener(handler)
        res = opener.open('https://order.jd.com/center/list.action')
        print res.read()


cookies=JdCookie()
cookies.loginSaveCookie()
cookies.getCookie()
