#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 10:04:14 2024

@author: kate
"""

# 爬找google、yahoo，由使用者輸入搜尋關鍵字，印出標題、連結與平台，分別爬找5頁內容

import requests
from bs4 import BeautifulSoup
import pandas as pd

keyword = input("請輸入欲搜尋的關鍵字:")
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15'}

titleL = []
linkL = []
platform = []
keywordL = []

#google

for page in range(5):
    params = {"start": page*10}
    
    r = requests.get("https://www.google.com/search?q={}".format(keyword), headers=headers, params=params)
    
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        
        titles = soup.find_all('h3', class_='LC20lb MBeuO DKV0Md')
        links = soup.find_all('a', attrs={'jsname':'UWckNb'})
    
        for title,link in zip(titles,links):
            titleL.append(title.text)
            linkL.append(link.get('href'))
            platform.append('Google')
            keywordL.append(keyword)
            
        #以select改寫
        titles = soup.select("h3.LC20lb.MBeuO.DKV0Md")
        links = soup.select("div.yuRUbf a")
        for title,link in zip(titles,links):
            print(title.text)
            print(link.get('href'))
            print()
           
# yahoo

    params = {'b': (page*7)+1}
    r = requests.get("https://tw.search.yahoo.com/search?p={}".format(keyword), headers=headers, params=params)
    
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        
        titles = soup.find_all('h3', class_='title tc')
        
        for title in titles:
            titleL.append(title.a.get('aria-label'))
            linkL.append(title.a.get('href'))
            platform.append('Yahoo')
            keywordL.append(keyword)
    
        #以select改寫
        titles = soup.select("h3.title a")
        for title in titles:
            print(title.get('aria-label'))
            print(title.get('href'))
            print()
            
# 存成csv檔
result = pd.DataFrame({"Title":titleL, "Link":linkL, "Playform":platform, "Keyword":keywordL})
result.to_csv("SearchEngine.csv")





            