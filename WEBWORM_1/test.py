#encoding:utf-8

import json
import requests
from bs4 import BeautifulSoup
import re
import threading
import time
'''
dc = {'a':1,'b':2,'c':3}
d = 'b'
print(dc[d])
'''

'''
url = 'https://tieba.baidu.com/p/totalComment?t=1502638268424&tid=4228190883&fid=267312&pn=1&see_lz=0'
data = requests.get(url)
js = json.loads(data.text)
ds = js['data']['comment_list']
print(type(ds))

for d in ds:
    print("################")
    print(d)
    for i in ds[d]['comment_info']:
        print(i['username'])
        #print(ds[d]['comment_info'][i]['username'])
'''



def func():
    for i in range(0,3):
        print("1")
        time.sleep(1)
    return
ths = []
for i in range(0,10):
    th = threading.Thread(target=func,args=(),name='name'+str(i))
    th.start()
    ths.append(th)

while len(ths)>0:
    th = ths.pop()
    th.join()
    print("got")

print("##############################for end###################################")