#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 13:34:19 2024

@author: kate
"""

# 郵局郵遞區號網頁 自動輸入辨識碼(圖片)，再輸出郵遞區號與投遞範圍

import requests
from bs4 import BeautifulSoup

from PIL import Image
import pytesseract

def zipSearch(county, township, street):
    
    while True:
        session = requests.Session()
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15'}
        url = "https://www.post.gov.tw/post/internet/Postal/index.jsp?ID=130107"
        
        r = session.get(url, headers=headers)
        if r.status_code == 200:
            
            soup = BeautifulSoup(r.text, 'html.parser')
            
            img = soup.find('img',id='imgCaptcha3_zip6').get('src')[2:]
            vkey = img.split('vKey=')[1]
            imgUrl = "https://www.post.gov.tw/post/internet"+img
            rUrl = session.get(imgUrl, headers=headers)
            with open('ocrNum.jpg', 'wb') as f:
                for chunck in rUrl:
                    f.write(chunck)
        
            # pytesseract.pytesseract.tesseract_cmd ='/usr/local/bin/tesseract'
            img = Image.open('ocrNum.jpg')
            img = img.convert('L') # 轉灰階
            ans = str.strip(pytesseract.image_to_string(img, config='--psm 7'))
        
    
            url = "https://www.post.gov.tw/post/internet/Postal/index.jsp"
            params = {"ID":"130107",
                      "list": "5",
                      "list_type": "1",
                      "firstView": "3",
                      "vKey": vkey,
                      "city_zip6": county,
                      "cityarea_zip6": township,
                      "street_zip6": street,
                      "checkImange_zip6": ans,
                      "Submit": "查詢"
                      }
            
            r = session.post(url, headers=headers, data=params)
            if r.status_code == 200:
                if "驗證碼輸入錯誤" in r.text:
                    continue
    
                soup = BeautifulSoup(r.text, 'html.parser')
                # print(soup)
                zips = soup.find_all('td', attrs={'data-th':'郵遞區號'})
                areas = soup.find_all('td', attrs={'data-th':'投遞範圍'})
                for code, area in zip(zips, areas):
                    print(code.text, area.text)
                break
            
county = input("請輸入想搜尋的縣市：")
if "台" in county:
    county = "臺"+county[1:]
    
township = input("請輸入想搜尋的鄉鎮[市]區：")
street = input("請輸入想搜尋的路(街)名或鄉里：")
zipSearch(county, township, street)   




    