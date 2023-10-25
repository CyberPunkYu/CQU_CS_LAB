#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Filename: test_new.py
import urllib.request

#获取一个get请求

# response = urllib.request.urlopen("http://www.baidu.com")
# print(response.read().decode('utf-8'))  #对获取到的网页源码进行utf-8解码
# #print(response.read())


import urllib.request
reponse = urllib.request.urlopen('http://www.baidu.com')
print(reponse.read().decode('utf-8'))

#1. 获取网页   check    urllib      (n-1)*25
#2. 解析数据       正则+scrapy bs4   selume  xpath
#3. 存储  check    execl  txt  json  db