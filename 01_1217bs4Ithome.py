#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 14:41:14 2024

@author: kate
"""

import requests
from bs4 import BeautifulSoup
r = requests.get("https://www.ithome.com.tw/")


if r.status_code == 200:
    
    soup = BeautifulSoup(r.text, 'html.parser')

    titles = soup.find_all('p', class_='title')
    dates = soup.find_all('p', class_='post-at')

    for title,date in zip(titles, dates):
        
        print(title.text)
        print(date.text)
        print("https://www.ithome.com.tw{}".format(title.a.get('href')))
        print()
        
        
    #way2
    for title,date in zip(titles, dates):
        soup2 = BeautifulSoup(str(title), 'html.parser')
        
        print(title.text)
        print(date.text)
        # 因為a只有一個，所以不用用find_all再跑迴圈
        print("https://www.ithome.com.tw"+soup2.find('a').get('href'))
        print()
        