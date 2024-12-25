#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 16:35:45 2024

@author: kate
"""

# 爬找PTT表特版 (以select方式)
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import os

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15'}
params = {'from': '/bbs/gossiping/index.html', 'yes':'yes'}

def pttImg(keyword, count):
    session = requests.session()
    session.post('https://www.ptt.cc/ask/over18', headers=headers, data=params)
    
    url = 'https://www.ptt.cc/bbs/Beauty/index.html'
    os.makedirs(keyword, exist_ok=True)
    c = 0
    
    while True:
        
        r = session.get(url, headers=headers)
        
        if r.status_code == 200:
            soup = BeautifulSoup(r.text.split('r-list-sep')[0], 'html.parser')
            
            titles = soup.select('div.r-ent')
            # dates = soup.select('div.date')
            
            # 準備上一頁的url
            nextUrl = soup.select('a.btn.wide')[1].get('href')
            url = "https://www.ptt.cc"+nextUrl  
            
            
            for t in titles[::-1]:
                #如果是回復文或刪除文章跳過
                if "Re:" in t.text or "刪除)" in t.text:
                    continue
                
                title = t.a.text
                if keyword in title:
                    link = "https://www.ptt.cc"+t.a.get('href')
                    # date = d.text
                    
                    print(title, link)               
                    
                    
                    try:
                        #進入每篇抓取文章內容(圖片連結)
                        r2 = session.get(link, headers=headers)
                        soup2 = BeautifulSoup(r2.text, 'html.parser')
                        contents = soup2.select_one('div#main-content').text.split('--')[0].split('時間')[1].split('\n')[1::]
    
                        for imgUrl in contents:
                            string = imgUrl.lower()
                            pattern = "^https\S*([.](jpg|png|gif|jpeg)$)"
                            if re.findall(pattern, string):
                                fileName = imgUrl[imgUrl.rfind("/")+1:]
                                print(fileName)
                                rUrl = requests.get(imgUrl, headers=headers)
                                with open("./"+keyword+"/"+fileName, "wb") as fileWrite:
                                    
                                    for chunck in rUrl:
                                        fileWrite.write(chunck)
                                c += 1
                                if c == count:
                                    return
                                    
                            else:
                                continue
                      
                    except:
                        pass
                

while True:
    keyword = input("請輸入想抓取的關鍵字(或按Q離開)：")
    if keyword == "q" or keyword == "Q":
        break
    
    else:
        count = eval(input("請輸入想搜尋幾張："))
        pttImg(keyword, count)



