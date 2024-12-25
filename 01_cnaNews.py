#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 25 15:56:12 2024

@author: kate
"""


import requests
from bs4 import BeautifulSoup

def catchTime(link):
    r = session.get(link, headers=headers)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        try:
            updateTime = soup.select_one('div.updatetime span').text
            
        
        except:
            updateTime = soup.select('div.mainDetail p')[1].text[:16]
        
        return updateTime
    

# 中央社首頁新聞
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15"}
url = "https://www.cna.com.tw"

session = requests.Session()

r = session.get(url, headers=headers)

if r.status_code == 200:
    soup = BeautifulSoup(r.text, 'html.parser')
    
    #編輯台推薦
    topNews = soup.select('div#NewsTopic a')
    for news in topNews:
        title = news.h2.text
        link = "https://www.cna.com.tw"+news.get('href')
        updateTime = catchTime(link)
        print(updateTime, title, link)
        
    #特派看世界
    worldNews = soup.select('div#OverseasWorld a')
    for news in worldNews:
        title = news.h2.text
        link = "https://www.cna.com.tw"+news.get('href')
        updateTime = catchTime(link)
        print(updateTime, title, link)
        
    #解釋性新聞
    explainNews = soup.select('div.Interpretation a')[2:]
    for news in explainNews:
        title = news.h2.text
        link = "https://www.cna.com.tw"+news.get('href')
        updateTime = catchTime(link)
        print(updateTime, title, link)
        
    #新聞圖表
    chartNews = soup.select('div.Chart a')[2:]
    for news in chartNews:
        title = news.h2.text
        link = "https://www.cna.com.tw"+news.get('href')
        updateTime = catchTime(link)
        print(updateTime, title, link)
    
