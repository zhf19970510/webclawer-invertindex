from bs4 import BeautifulSoup
import requests
import os
import re
os.chdir(r'F:\Python 学习\python_课件+实验指导书\lab\website')
file=["11.txt","21.txt","22.txt","23.txt","24.txt","31.txt","32.txt","41.txt"]
store={}
counts={}
#读取文本内容
def read_context():
    f=open("21.txt","r")
    #找到文件里所对应所有P标签的内容，并将它们存储下来
    f.readline()
    f.readline()
    text=f.read()
    f.close()
    return text
#然后用soup分析文档内容，找出p标签的所有内容
def parse(text):
    soup=BeautifulSoup(text,"html.parser")
    data1=""
    p=soup.find_all("p")
    for data in p:
        #print(data.string)
        data=data.string
        data1=data1+data
    return data1
#字符串转化为列表类型
def stringToList(data1):
    words = re.sub("[,.?!#$%&()*+-/:;<=>?@]", "",data1)
    words=words.strip().split()
    print(words)
    return words
#词频统计
def word_count(words):
    for word in words:
        counts[word]=counts.get(word,0)+1
    return counts
#实现倒排索引
def inverted_index(counts):
    for key  in counts:
        if key in store:
            store[key].append(["21.txt",counts[key]])
        else:
            store[key]=["21.txt",counts[key]]
    return store
#词频由高到低进行排序
def word_sort(counts):
    items=list(counts.items())
    items.sort(key=lambda x:x[1],reverse=True)
    return items
#找出内容后，对单词进行分片split统计，单词可以用set来表现出来，使得单词
#独立出现，易于统计。可以用列表进行存储，易于遍历。然后对单词出现的次数
#进行统计，可以用字典进行存储。
#然后用标准格式进行存储，即总体而言，有比如：['you',['11.txt',次数]
#然后再由系统输入一个单词，然后遍你相应的字典内容，然后判断次数是否大于0,大于0
#则取出文件并读出链接内容。
#然后将链接内容输出。

if (__name__ == '__main__'):
    text=read_context()
    data1=parse(text)
    words=stringToList(data1)
    counts=word_count(words)
    print(counts)
    items=word_sort(counts)
    print(items)
    for i in range(len(items)):
        word,count=items[i]
        print("{0:<10}{1:>5}".format(word,count))
    
    inverted_index(counts)
    print(store)
