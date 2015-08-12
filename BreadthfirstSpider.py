#-*-coding:utf-8-*-
#-------------------------------------
# Name:     Breadth_first_spider(宽度优先爬虫)
# Purpose: 
# Author:   xuxiaoqing
# Date:     2015.8.4
#-------------------------------------

import urllib2,re,socket
from bs4 import BeautifulSoup

# deep = 30
class LinkQueue:

    def __init__(self):
        #pass
        self.visited = []#已访问的url集合
        self.unvisited = []#待访问的url集合
        
        
    def addvisitedurl(self,url):#添加到访问过得url队列中
        self.visited.append(url)
        
    def addunvisitedurl(self,url):#保证每个url只被访问一次
        if url !="" and url not in self.visited and url not in self.unvisited:
            self.unvisited.insert(0,url)
        
    def getvisitedurl(self):#获取访问过的url队列
        return self.visited
        
    def getunvisitedurl(self):#获取未访问的url队列 
        return self.unvisited
        
    def removevisitedurl(self,url):#移除访问过得url
        return self.visited.remove(url)
        
    def unvisitedurldequeue(self):#未访问过得url出队列
        try:
            return self.unvisited.pop()
        except:
            return None
            
    def getvisitedurlcount(self):#获得已访问的url数目
        return len(self.visited)
        
    def getunvisitedurlcount(self):#获得未访问的url数目
        return len(self.unvisited)
        
    def unvisitedurlsempty(self):#判断未访问的url队列是否为空
        return len(self.unvisited)==0
    

class CrawlSpider:
        
    def __init__(self,seeds):
        self.LinkQueue=LinkQueue() #使用种子初始化url队列
        if isinstance(seeds,str):  
            self.LinkQueue.addunvisitedurl(seeds)  
        if isinstance(seeds,list):  
            for i in seeds:  
                self.LinkQueue.addunvisitedurl(i)  
        # self.iscontrol = False
        # if deep!=0:
            # self.iscontrol = True
        # self.deep = 0
        print self.LinkQueue.unvisited
        print self.LinkQueue.getvisitedurlcount()
        print len(self.LinkQueue.unvisited)
        print "Add the seeds url \"%s\" to the unvisited url list"%str(self.LinkQueue.unvisited)
        
    def crawling(self,seeds,crawl_count):#抓取过程主函数
        while self.LinkQueue.unvisitedurlsempty() is False and self.LinkQueue.getvisitedurlcount()<= crawl_count:#循环条件：待抓取的链接不空且专区的网页不多于crawl_count
            visiturl = self.LinkQueue.unvisitedurldequeue()#队头url出队列
            print "Pop out one url \"%s\" from unvisited url list"%visiturl 
            if visiturl is None or visiturl =="":
                continue
            links = self.getnewlinks(visiturl)#获取visteurl中的链接
            print "Get %d new links"%len(links)
            self.LinkQueue.addvisitedurl(visiturl)#将visteurl放入已访问队列
            print "Visited url count: "+str(self.LinkQueue.getvisitedurlcount()) 
            for link in links:
                self.LinkQueue.addunvisitedurl(link)#将获取的链接放入待访问的队列
            print "%d unvisited links:"%len(self.LinkQueue.getunvisitedurl())
                
    def getnewlinks(self,url):
        # self.deep += 1
        links = []
        data = self.getpagesource(url)#获取网页源码
        if data[0]=="200":   
            soup=BeautifulSoup(data[1])  
            a=map(lambda e: e.get('href'),soup.find_all('a',href=re.compile(r'^http')))  #获取网页源码中的链接
            for i in a:  
                links.append(i)   
        return links  
        
    def getpagesource(self,url,timeout=100,coding=None):
        try:
            socket.setdefaulttimeout(timeout) 
            req = urllib2.Request(url)
            req.add_header('User-agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')  
            response = urllib2.urlopen(req) 
            if coding is None:  
                coding= response.headers.getparam("charset")  #获取网页编码方式
            if coding is None:  
                page=response.read()  
            else:  
                page=response.read()  
                page=page.decode(coding).encode('utf-8')  
            return ["200",page]  
        except Exception,e:  
            print str(e)  
            return [str(e),None] 

            
def main(seeds,crawl_count):  
    craw=CrawlSpider(seeds)  
    craw.crawling(seeds,crawl_count) 
    
if __name__=="__main__":  
    main("http://www.baidu.com",50)     