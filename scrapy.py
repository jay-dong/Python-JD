#!/usr/bin/env python
#coding=utf8
import urllib2
import time
import lxml.html
import scrapy
from bs4 import BeautifulSoup
import re
from pymongo import MongoClient
def  Mongo(ip='127.0.0.1',port='27017',databases='local'):

    client=MongoClient(ip,27017)
    db=client.databases
    return db

#   url =  抓去的url         user_agent   =  代理信息
def download(url,user_agent='wssp',num=5):

    print '爬虫开始：',url

    headers={'User_agent':user_agent}
    request=urllib2.Request(url,headers=headers)
    try:
        html=urllib2.urlopen(request).read()
    except urllib2.URLError as e:

        if hasattr(e,'code') and e.code>400:

            log=open('python.log','wb')
            log.close()
        html=None
    return html
#正则提取
def reData(html):
    print html
    return re.findall('<div class="company">(.*？)</div>',html)

#beautifulsoup提取

def soup(html,page=1):
    soup=BeautifulSoup(html,'html.parser')
    ul=soup.find_all('ul',attrs={'class':'item_con_list'})
    ul=ul[1]
    li=ul.find_all('li',attrs={'class':'con_list_item'})
    if page==1:

        page=soup.find_all('a',attrs={'class':'page_no'})
        page=page[-2].text

    company=[]

    for ele in li:

        div=ele.find('div',attrs={'class':'list_item_top'})
        #公司名
        company=div.find('div',attrs={'class':'company'}).find('div',attrs={'class':'company_name'})
        text=company.text
        text=re.sub('\n','',text)
        #学历要求 && 学历
        education=div.find('div',attrs={'class':'position'}).find('div',attrs={'class':'p_bot'}).find('div',attrs={'class','li_b_l'})
        education=education.text
        education=re.sub('\n','',education)
        #薪资待遇
        money=div.find('div',attrs={'class':'position'}).find('div',attrs={'class':'p_bot'}).find('div',attrs={'class','li_b_l'}).find('span',attrs={'class':'money'})
        money=money.text
        money=re.sub('\n','',money)
        #公司类型
        comtype=div.find('div',attrs={'class':'company'}).find('div',attrs={'class':'industry'})
        comtype=comtype.text
        comtype=re.sub(' \s','',comtype)
        db=Mongo()
        db.company.insert({'name':text,'education':education,'money':money,'comtype':comtype})
        company.append(div.text)
    
    return company
#lxml
def xmlData(html):

    tree=lxml.html.fromstring(html)
    data=tree.cssselect('li.con_list_item > div.list_item_top > div.position')
    listData=[]
    for k in data:

        Ele=k.text_content()
        listData.append(Ele)
    return listData


i=1;
while i<=30:
    html=download('https://www.lagou.com/zhaopin/PHP/'+str(i),'Baiduspider')
    soup(html)
    i+=1



