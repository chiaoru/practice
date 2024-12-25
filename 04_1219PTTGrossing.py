#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 14:45:25 2024

@author: kate
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15'}
params = {'from': '/bbs/gossiping/index.html', 'yes':'yes'}

titleL = []
dateL = []
urlL = []
contentL = []

# 以function 方式讓日期不等於要抓取的時間時，直接跳出
def ptt():
    session = requests.Session()
    
    session.post('https://www.ptt.cc/ask/over18', headers=headers, data=params)
    getDate = input("請輸入想抓取的日期：MM/DD: ")
    url = 'https://www.ptt.cc/bbs/gossiping/index.html'
    
    while True:
        r = session.get(url, headers=headers)
        
        if r.status_code == 200:
            soup = BeautifulSoup(r.text.split("r-list-sep")[0], 'html.parser')
            titles = soup.find_all('div', class_='title')
            dates = soup.find_all('div', class_='date')
            
            nextUrl = "https://www.ptt.cc"+soup.select('a.btn.wide')[1].get('href')
            url = nextUrl
            
            # 從下往上抓取
            for title,date in zip(titles[::-1],dates[::-1]):
                if "Re:" in title.text or "刪除)" in title.text:
                    continue
                
                d = date.text.strip()
                t = title.text.strip()
                print(d, t)
                # 只抓當天日期
                # if date.text.strip() != getDate:
                #     return
                
                # 抓到哪一個日期為止
                if d == getDate:
                    return
                
                
                dateL.append(d)
                titleL.append(t)
                urlL.append("https://www.ptt.cc"+title.a.get('href'))
                
                try:
                    r2 = session.get("https://www.ptt.cc"+title.a.get('href'), headers=headers)
                    soup2 = BeautifulSoup(r2.text, 'html.parser')
                    content = soup2.find('div',id='main-content').text.split('--')[0].split('2024')[1]
                    contentL.append(content)
                    
                    # 老師解
                    # upSplit = soup2.select('span.article-meta-value')[3].text
                    # downSplit = "※ 發信站"
                    # temp = soup2.select_one('div#main-content').text.split(upSplit)[1].split(downSplit)[0]
                    # result = temp[2:-4]
                    # print(result)
                    
                    
                
                except:
                    contentL.append("內容無法顯示。")
                    # pass
    
    
ptt()

# 存成csv檔
result = pd.DataFrame({"Date":dateL, "Title":titleL, "Link":urlL, "Content":contentL})
result.to_csv("PTTGossiping.csv")




        