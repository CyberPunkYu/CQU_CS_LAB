#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Filename: try.py

import urllib.request,urllib.error

def askURL(url):
    head = {                #模拟浏览器头部信息，向豆瓣服务器发送消息
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
    }
                            #用户代理，表示告诉豆瓣服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接收什么水平的文件内容）

    request = urllib.request.Request(url,headers=head)  #使用request封装url和头部信息
    html = ""
    #异常处理
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
   # return html

def main():
    baseurl = "https://movie.douban.com/top250?start="
    askURL("https://movie.douban.com/top250?start=0")

if __name__ == "__main__":          #当程序执行时
#调用函数
    main()
