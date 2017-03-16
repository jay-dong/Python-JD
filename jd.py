#!usr/bin/env python
#coding=utf8
import json
import demjson
from lxml import etree
import urllib2
import urllib
import httplib
from future.builtins import int
import multiprocessing
import thread
from pymongo import MongoClient
from zope.interface.common.interfaces import IIOError
import sys
import os
import time
reload(sys)
sys.setdefaultencoding( "utf-8" )
'''
    写的有点乱哈，仅使用玩耍
    正常开发别和我这样写哦
    header项的cookie必须加上，具体原因就不说明了
'''
class Jd:
    
    def __init__(self,url):

        header={
            'User-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Cookie':''
        }
        request=urllib2.Request(url,headers=header)
        html=urllib2.urlopen(request).read()
        html=html.decode('utf-8')
        self.url=url
        self.selector=etree.HTML(html)
        self.html=html
        self.id=1
    def __mongo(self):
        
        client=MongoClient('127.0.0.1',27017)
        db=client.jd
        return db
    #获取品牌信息
    def getBrandList(self):
        
        return self.html
    #获取页数
    def getGoodsPage(self):
        selector=self.selector
        div=selector.xpath("//div[@id='J_bottomPage']/span")
        if div==[]:
            page=1
        else:
            div=div[1]
            page=div.xpath("./em/b/text()")
            page=int(page[0])
        return page
    #获取商品编号
    def goodsInfo(self,brandId,name):
         # print self.url
         # html=urllib2.urlopen("https://list.jd.com/list.html?cat=9987,653,655&ev=exbrand_8557&sort=sort_rank_asc&trans=1&page=1#J_crumbsBar").read()
         # html=html.decode('utf-8')
         # fil=open('1.html','wb')
         # fil.write(self.html)
         # fil.close()
         # html=etree.HTML(html)
         goodsId=self.selector.xpath("//div[@id='plist']/ul/li/div/@data-sku")
         goodsName=self.selector.xpath("//a[@target='_blank']/em/text()")
         data=dict(zip(goodsId,goodsName))
         db=self.__mongo()
         for id in data:
             date=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
             print data[id]
             try:
                db.boy.insert({'BrandId':brandId,'brandName':name,'GoodsName':data[id],'GoodsId':id,'url':self.url,'date':date})
                self.id+=1
                 #print '写入成功id:'+str(id)
             except IOError as e:
                 print e.rason
         #goodsName=selector.xpath("//div[@id='plist']/ul/li/div/div[@class='p-name']/a/em/text()")
    #获取商品名称
    def __getGoodsInfo(self,goodIdList):
        pass
    
    #获取商品介绍
    def __getGoodsDesc(self):
        pass
    
    #获取商品价格
    def __getGoodsInfo(self):
        pass
    
    def __call__(self,url):
        pass
    
JD=Jd('https://list.jd.com/list.html?cat=1315,1342&page=1&sort=sort_totalsales15_desc&trans=1&md=1&my=list_brand')
brand=JD.getBrandList()
brand=json.loads(brand)
if __name__=="__main__":
    #n=0
    #while n<4:    
    for ur in brand['brands']:
        print '开始品牌：'+ur['name']
        url="https://list.jd.com/list.html?cat=1315,1342&ev=exbrand_"+str(ur['id'])+'&sort=sort_totalsales15_desc&trans=1&JL=6_0_0#J_main'
        print url
        jdpage=Jd(url)
        page=jdpage.getGoodsPage()
        i=1
        while i<=page: 
            jdList=Jd('https://list.jd.com/list.html?cat=1315,1342&ev=exbrand_'+str(ur['id'])+'&page='+str(i)+'&sort=sort_totalsales15_desc&trans=1&JL=6_0_0#J_main')
            # p=multiprocessing.Process(target=jdList.goodsInfo,args=(brandId,str(brand[ur])))
            # p.start()
            # p.join
            thread.start_new_thread(jdList.goodsInfo,(ur['id'],str(ur['name'])))
            #jdList.goodsInfo(brandId,str(brand[ur]))
            i+=1
            
        #n+=1     
        #print JD.getGoodsPage()
