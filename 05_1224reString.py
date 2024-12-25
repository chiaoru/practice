#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 10:39:49 2024

@author: kate
"""
# 用正則表達式改寫字串驗證：

import re

# 身分證字號驗證: 使用者輸入身分證字號，如打錯從新輸入
# 共10個字，第一個字為大寫英文，第一個數字為1或2，後面8碼為數字


while True:
    
    ID = input("請輸入您的身分證字號：")
    pattern = "^[A-Z][1-2]\d{8}"
    string = ID
    
    if re.findall(pattern, string):
        print("{}，身分證驗證成功".format(ID))
        break

    else:
        print("身分證輸入錯誤，請重新輸入：")
        
# 手機號碼驗證
# 10個數字，開頭為09

while True:
    phone = input("請輸入您的電話號碼：")
    pattern = "^0{1}9{1}\d{8}"
    if re.findall(pattern, phone):
        print("{}，電話驗證成功".format(phone))
        break
    else:
        print("電話號碼錯誤，請重新輸入：")
        
        
# email 驗證
# 必須有@，結尾必須為 .com

while True:
    email = input("請輸入您的Email：")
    pattern = "\S*@\S*([.]com)$"
    if re.findall(pattern, email):
        print("{}，Email驗證成功".format(email))
        break
    else:
        print("Email錯誤，請重新輸入：")
        