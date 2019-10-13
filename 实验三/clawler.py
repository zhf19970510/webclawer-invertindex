#encoding=utf-8
import requests
import os
from bs4 import BeautifulSoup
import re
#运行服务器语句：python -m http.server 8000
os.chdir(r'F:\Python 学习\python_课件+实验指导书\lab\实验三')
filenames=[]
class MyCrawler:
    def __init__(self,seeds):
        #使用种子初始化url队列
        self.linkQuence=linkQuence()
        if isinstance(seeds,str):
            self.linkQuence.addUnvisitedUrl(seeds)
        if isinstance(seeds,list):
            for i in  seeds:
                self.linkQuence.addUnvisitedUrl(i)
        print("Add the seeds url \"%s\" to the unvisited url list"%str(self.linkQuence.unVisited))

        #抓取过程主函数
    def crawling(self,seeds,crawl_count):
        #循环条件:待抓取的链接不空且专区的网页不多于crawl_count
        count=0                     #用于记录未访问队列中当前层次还有几个链接未访问
        DicVisited={}                #每一层对应有几个子链接
        DicVisited[1]=1
        n=1                         #用于记录字典下标，代表第几层
        fileno=0
        while self.linkQuence.unVisitedUrlIsEmpty() is False and\
            self.linkQuence.getVisitedUrlCount()<=crawl_count:
            #队头url出队列
            visitUrl=self.linkQuence.unVisitedUrlDeQuence()
            state,page=self.getPageSource(visitUrl)
            
            print("Pop out one url \"%s\" from unvisited url list"
                  %visitUrl)
            if visitUrl is None or visitUrl=="":
                continue

            #获取超链接
            links=self.getHyperLinks(visitUrl)
            print("Get %d new links"%len(links))
            #将url放入已访问的url中
            self.linkQuence.addVisitedUrl(visitUrl)
            print("Visited url count: "+str(self.linkQuence.
                                                getVisitedUrlCount()))
            #未访问的url入列
            for link in links:
                self.linkQuence.addUnvisitedUrl(link)
            print("%d unvisited links:"%len(self.linkQuence.
                                            getUnvisitedUrl()))
            level=len(DicVisited)
            fileno=DicVisited[n]-count
            filename=str(level)+str(fileno)+".txt"
            filenames.append(filename)
            filename=open(filename,'w+')
            filecontent=[str(visitUrl)+"\n",str(level)+"\n",str(page)+"\n"]
            filename.writelines(filecontent)
            filename.close()
            if count==0:
                tmp=self.linkQuence.getUnvisitedUrlCount()
                n+=1
                DicVisited[n]=count=tmp
            count-=1
        
        

    #获取源码中的超链接
    def getHyperLinks(self,url):
        links=[]
        data=self.getPageSource(url)
        if data[0]=="200":
            soup=BeautifulSoup(data[1],"html.parser")
            a=soup.find_all("a",{'href':re.compile(".*")})
            #print(a)
            for i in a:
                if i["href"].find("http://")!=-1:       #找到复杂地址直接跳过
                    continue
                print(i["href"])
                links.append("http://127.0.0.1:8000"+i["href"])
        return links

    #获取网页源码
    def getPageSource(self,url):
        try:
            req=requests.get(url,timeout=30)
            req.raise_for_status()                        #如果状态不是200,引发异常
            req.encoding='utf-8'                          #无论原来用什么编码,都改成utf-8
            f=req.text
            return ["200",f]
        except Exception as e:
            print(str(e))
            return [str(e),None]

def getFilenames():
    return filenames

class linkQuence:
    def __init__(self):
        #已访问的url集合
        self.visited=[]
        #待访问的url集合
        self.unVisited=[]
        #获取访问过的url队列
    def getVisitedUrl(self):
        return self.visited
    #获取未访问的url队列
    def getUnvisitedUrl(self):
        return self.unVisited
    #添加到访问过的url队列
    def addVisitedUrl(self,url):
        self.visited.append(url)
    #移除访问过的url
    def removeVisitedUrl(self,url):
        self.visited.remove(url)
    #未访问过的url出队列
    def unVisitedUrlDeQuence(self):
        try:
            return self.unVisited.pop()
        except:
            return None
    #保证每个url只被访问一次
    def addUnvisitedUrl(self,url):
        if url!="" and url not in self.visited and url not in self.unVisited:
            self.unVisited.insert(0,url)
    #获得已访问的url数目
    def getVisitedUrlCount(self):
        return len(self.visited)
    #获得未访问的url数目
    def getUnvisitedUrlCount(self):
        return len(self.unVisited)
    #判断未访问的url队列是否为空
    def unVisitedUrlIsEmpty(self):
        return len(self.unVisited)==0


def main(seeds,crawl_count):
    craw=MyCrawler(seeds)
    craw.crawling(seeds,crawl_count)

if __name__=="__main__":
    main("http://127.0.0.1:8000/index.html",50)
    filenames=getFilenames()
    print(filenames)
            

    
