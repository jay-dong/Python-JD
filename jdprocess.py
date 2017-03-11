#!usr/bin/env python
#coding=utf8
import json
from lxml import etree
import urllib2
from future.builtins import int
import multiprocessing
import thread
from pymongo import MongoClient
from zope.interface.common.interfaces import IIOError
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
class Jd:
    
    def __init__(self,url):

        header={'User-agent':'HuihuiSpider'}
        request=urllib2.Request(url,headers=header)
        html=urllib2.urlopen(request).read()
        html=html.decode('utf-8')
        self.url=url
        self.selector=etree.HTML(html)
        self.html=html
    def __mongo(self):
        
        client=MongoClient('127.0.0.1',27017)
        db=client.jd
        return db
    #获取品牌信息
    def getBrandList(self):
        dic={}
        brand={}
        brandId=self.selector.xpath("//ul[@id='brandsArea']/li/@id")
        brandName=self.selector.xpath("//ul[@id='brandsArea']/li/a/@title")
        data=dict(zip(brandId,brandName))
        return data
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
         db=self.__mongo()
         
         for id in goodsId:
             print id
             try:
                 db.goods.insert({'BrandId':brandId,'brandName':name, 'GoodsId':id})
                # print '写入成功id:'+str(id)
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
    
JD=Jd('https://list.jd.com/list.html?cat=9987,653,655')
brand=JD.getBrandList()
if __name__=="__main__":
    n=0
    while n<4:
        for ur in brand:
            
            brandId=ur.lstrip("brand-")
            url="https://list.jd.com/list.html?cat=9987,653,655&ev=exbrand_"+brandId
            jdpage=Jd(url)
            page=jdpage.getGoodsPage()
            i=1
            while i<page: 
                jdList=Jd(url+'&page='+str(i))
                #print url+'&page='+str(i)
                p=multiprocessing.Process(target=jdList.goodsInfo,args=(brandId,str(brand[ur])))
                p.start()
                p.join
#                 thread.start_new_thread(jdList.goodsInfo,(brandId,str(brand[ur])))
#                 jdList.goodsInfo(brandId,str(brand[ur]))
                i+=1
        n+=1     
        #print JD.getGoodsPage()
