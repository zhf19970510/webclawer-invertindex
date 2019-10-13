from bs4 import BeautifulSoup
import os
import re


path=os.chdir('F:\Python 学习\python_课件+实验指导书\lab\实验三')
filenames=[]            #查找指定目录下的txt文件，并用filenames存储
store={}                #store用于存储倒排索引的结果
#读取文本内容
def read_context(file):
    f=open(file,"r")
    #找到文件里所对应所有P标签的内容，并将它们存储下来
    text=f.read()
    f.close()
    return text
#然后用soup分析文档内容，找出p标签的所有内容
def parse(text):
    soup=BeautifulSoup(text,"html.parser")
    data1=""
    p=soup.find_all("p")
    for data in p:
        data=data.string
        data=data.lower()
        data1=data1+" "+data
    return data1
#字符串转化为列表类型
def stringToList(data1):
    words = re.sub("[,.?!#$%&()*+-/:;<=>?@]", "",data1)
    words=words.strip().split()
    #print(words)
    return words
#词频统计
def word_count(words):
    counts={}               #counts用于记录每个文件的字典，即{'单词':次数}
    for word in words:
        counts[word]=counts.get(word,0)+1
    return counts
#实现倒排索引
def inverted_index(file,counts):
    for key  in counts:
        if key in store:
            store[key].append([file,counts[key]])
        else:
            store[key]=[[file,counts[key]]]
    return store
#词频由高到低进行排序
def word_sort(ls):
    ls.sort(key=lambda x:x[1],reverse=True)
    return ls
#找到指定目录下的txt文件，即爬虫之后保存的文件
def find_files():
    items=os.listdir(path)
    for names in items:
        if names.endswith(".txt"):
            filenames.append(names)
    return filenames


if (__name__ == '__main__'):
    #开始整体进行操作：
    filenames=find_files()
    for file in filenames:
        text=read_context(file)
        data1=parse(text)
        words=stringToList(data1)
        counts=word_count(words)
        store=inverted_index(file,counts)
    print(store)                    #倒排索引后的结果
    while True:
        keyword=input("请输入需要查找的关键词：")
        if keyword==' ':
            print("程序结束")
            break
        print()
        keyword=keyword.lower()         #将关键字转为小写，统一查找
        ls=[]
        find_file=''                    #获取关键字所对应的文件名
        if keyword in store:
            ls=store[keyword]
            word_sort(ls)
            for element in ls:
                find_file=element[0]
                fl=open(find_file,'r')
                link=fl.readline()
                print(link)
        else:
            print("在指定服务网站中没有找到对应的关键字。")
            
        
