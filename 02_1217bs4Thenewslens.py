#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 15:50:49 2024

@author: kate
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup

addr = "https://www.thenewslens.com"
r = requests.get(addr)

category = ['music', 'lifestyle', 'society']

titleL = []
dateL = []
linkL = []
classL = []

    
for i in category:
    
    for page in range(1, 11):
        my_params = {"page": page}
        r = requests.get(addr+"/category/"+i, params=my_params)
        # print(r.url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
        
            titles = soup.find_all('h3')
            dates = soup.find_all('time')
            
            
            for title, date in zip(titles,dates):
                titleL.append(title.text.strip())
                dateL.append(date.text)
                linkL.append(title.a.get('href'))
                classL.append(i)
    
                print(title.text.strip())
                # print(date.text)
                # print(title.a.get('href'))


df = pd.DataFrame({"Title": titleL, "Link":linkL, "Times":dateL, "Class":classL})

df.to_csv('theNewsLens.csv', encoding='utf-8')

        
