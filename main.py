#encoding:utf-8
import requests
from bs4 import BeautifulSoup
import re
import random
from bson.dbref import DBRef
from MGDB import MGDB
import json
import threading
import time

def commentpage(href,dc,authorid):
    data = requests.get(href)
    js = json.loads(data.text)
    clists = js['data']['comment_list']
    for clist in clists:
        for info in clists[clist]['comment_info']:
            try:
                #'replier':dc[int(clist)]
                indata = {'author':DBRef(collection='author',id=authorid),'replier':DBRef(collection='reply',id=dc[int(clist)]),'commenter':info['user_id'],'time':info['now_time'],'user':info['username']}
                db.insertdata('comment',indata)
            except:
                print('####################')
                print('href:')
                print(href)
                print('dc:')
                print(dc)
                print('clist')
                print(clist)
                print('info')
                print(info)
                print('####################')
    return

#ret = cref.insert({'ball':rnd,'addr':DBRef(collection='setpy',id=ids.pop())})
def RecordAuthor(p_userids, p_times, users):
    data = {'author':p_userids[0],'time':p_times[0],'user':users[0]}
    ret = db.insertdata("author",data)
    replyids = []
    replyids.append(ret)
    for i in range(1,len(p_userids)):
        indata = {'author':DBRef(collection='author',id=ret),'replier':p_userids[i],'time':p_times[i],'user':users[i]}
        r = db.insertdata('reply',indata)
        replyids.append(r)
    return (replyids,ret)

def RecordReplier(authorid,p_userids, p_times,users):
    replyids = []
    for i in range(0,len(p_userids)):
        indata = {'author':DBRef(collection='author',id=authorid),'replier':p_userids[i],'time':p_times[i],'user':users[i]}
        ret = db.insertdata('reply',indata)
        replyids.append(ret)
    return replyids

def GetPID(href):
    r = breq.findall(href)
    if r:
        return r[0]
    else:
        return 0

def GetPage(data):
    soup = BeautifulSoup(data.text,'html.parser')
    ad_page = soup.find_all('span',class_='red')
    pages = int(ad_page[len(ad_page) - 1].text)
    return pages

def IntoPage(data,pid):
    users = []
    userids = []
    times = []
    pids = []
    soup = BeautifulSoup(data.text,'html.parser')
    for div_author in soup.find_all('div',class_='d_author'):
        li_author = div_author.find('li',class_='d_name')
        l_userid = li_author.get('data-field')
        users.append(li_author.find('a',class_='p_author_name').text)
        userids.append(GetPID(l_userid))

    for div_time in soup.find_all('div',class_='post-tail-wrap'):#('span',class_='tail_info'):
        for spans in div_time.find_all('span',class_='tail-info'):
            if spans.text.find(':') != -1:
                times.append(spans.string)
                break
    #<div class="d_post_content j_d_post_content "
    #id="post_content_81078599210"> </div>
    for div_pid in soup.find_all('div',class_='d_post_content'):
        ret = int(breq.findall(div_pid.get('id'))[0])
        pids.append(ret)
    return (users, userids, times, pids)


def mainpage_req(l_href, pidref,pid):
    data = requests.get(l_href)
    (users, userids, times, pids) = IntoPage(data,pid)
    pages = GetPage(data)
    if pages <= 50:#begin grap if pages less than 100
        #author = userids[0]
        (replyids,authorid) = RecordAuthor(userids,times,users)
        c_href = 'https://tieba.baidu.com/p/totalComment?t=1502637646986&tid=' + str(pid) + '&fid=267312&pn=1&see_lz=0'
        dc = dict(zip(pids,replyids))
        commentpage(c_href, dc, authorid)
        if pages >= 2:
            for page in range(2,pages + 1):
                print(page)
                l_href = ''
                if pidref.find('fid=') != -1:
                    l_href = 'https://tieba.baidu.com' + pidref + '&pn=' + str(page)
                else:
                    l_href = 'https://tieba.baidu.com' + pidref + '?pn=' + str(page)

                data = requests.get(l_href)
                (users, userids, times, pids) = IntoPage(data,pid)
                replyids = RecordReplier(authorid,userids,times,users)
                c_href = 'https://tieba.baidu.com/p/totalComment?t=1502637646986&tid=' + str(pid) + '&fid=267312&pn=' + str(page) + '&see_lz=0'
                dc = dict(zip(pids,replyids))
                commentpage(c_href,dc,authorid)
    return
'''
users=[]
userids = []
times = []
pids = []
'''
breq = re.compile(r'\d+')
#<li class="d_name" data-field='{"user_id":40320073}'>
url = "https://tieba.baidu.com/f?kw=%E5%88%98%E6%85%88%E6%AC%A3&ie=utf-8&pn="
#IntoPage('https://tieba.baidu.com/p/5254722861',12345)
db = MGDB('127.0.0.1',27017,'walk68')
ths = []
for i in range(0,15001,50):
    data = requests.get(url + str(i))
    soup = BeautifulSoup(data.text,'html.parser')
    for thtit in soup.find_all('div',class_='threadlist_title'):
        pidref = thtit.a.get('href')
        print(thtit.a.get('title'))
        pid = GetPID(pidref)
        l_href = 'https://tieba.baidu.com' + pidref #+'?pn=1'
        #mainpage_req(l_href,pidref,pid)
        th = threading.Thread(target=mainpage_req,args=(l_href, pidref, pid))
        time.sleep(0.1)
        th.start()
        ths.append(th)
        #mainpage_req(l_href, pidref, pid)
    while len(ths)>0:
        th = ths.pop()
        th.join()
    print('Thread END !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
db.close()