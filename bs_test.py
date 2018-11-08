#coding=utf-8
#中文
import urllib.request
from bs4 import BeautifulSoup
import re
import time


def IntoPage(p_href):
    print(p_href)
    data = urllib.request.urlopen(p_href).read()
    soup = BeautifulSoup(data, "html.parser")
    s=soup.find(class_='phone-num')
    if s!=None:
        print(s.text)
        f.write(p_href+"\t"+s.text+"\r\n")
    else:
        f.write(p_href+"nothing\r\n")
    time.sleep(1)
    return

def mainpage(url):
    #url = "http://haikou.58.com/chuzu/pn1/?key=%25u4E2D%25u666F%25u82B1%25u56ED%25u79DF%25u623F&amp;minprice=0_2500&amp;sourcetype=5";
    data = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(data, "html.parser")
    reg = re.compile(r'entinfo=[0-9]+?_0&')

    for sgdiv in soup.find_all('div',class_='des'):
        sstr = sgdiv.a['href']
        ls = reg.findall(sstr)
        #print(len(ls))
        if len(ls)>0:
            s=ls[0][8:][:-3]
            p_href = 'http://haikou.58.com/zufang/'+ s + 'x.shtml'
            IntoPage(p_href)
        else:
            IntoPage(sstr)
        #http://haikou.58.com/zufang/30943534655543x.shtml

f=open("D:\phone2.txt","wt")
for i in range(1,7):
    #url="http://haikou.58.com/chuzu/pn" + str(i) + "/?key=%25u4E2D%25u666F%25u82B1%25u56ED%25u79DF%25u623F&amp";
    url="http://haikou.58.com/chuzu/pn" +str(i) + "/?PGTID=0d3090a7-0080-528a-a857-d252812f262b&ClickID=2"
    mainpage(url)
f.close();