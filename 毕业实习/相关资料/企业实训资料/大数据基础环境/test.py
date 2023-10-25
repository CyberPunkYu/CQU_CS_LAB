#!/usr/bin/python
# -*- coding:UTF-8 -*-
# Filename: test.py

import math
'''
模拟商场优惠打折，有三种优惠券可以用，**满减券**、**打折券**和**无门槛券**。

**满减券：满100减10，满200减20，满300减30，满400减40，以此类推不限制使用**；

**打折券：固定折扣92折，且打折之后向下取整，每次购物只能用1次**；

**无门槛券：一张券减5元，没有使用限制**。

每个人结账使用优惠券时有以下限制：

每人每次只能用两种优惠券，并且同一种优惠券必须一次用完，不能跟别的穿插使用（比如用一张满减，再用一张打折，再用一张满减，这种顺序不行）。

求不同使用顺序下每个人用完券之后得到的最低价格和对应使用优惠券的总数；如果两种顺序得到的价格一样低，就取使用优惠券数量较少的那个。


输入：第一行三个数字m,n,k，分别表示每个人可以使用的满减券、打折券和无门槛券的数量。
3 2 5
3
100
200
400

输出：
65 6
135 8
275 8
'''

m, n, k = map(int, input().split())
person = int(input())
price = []
# num = []
for i in range(person):
    price.append(int(input()))

def manjian(m, price, num):
    while((price >= 400) & (m >= 1)):
        price -= 40
        m -= 1
        num += 1
    while((price >= 300) & (m >= 1)):
        price -= 30
        m -= 1
        num += 1
    while((price >= 200) & (m >= 1)):
        price -= 20
        m -= 1
        num += 1
    while((price >= 100) & (m >= 1)):
        price -= 10
        m -= 1
        num += 1
    return price, num

def dazhe(price):
    price = price * 0.92
    # 向下取整
    return int(price)
    

def wumenkan(k, price):
    while(k >= 1):
        price -= 5
        k -= 1
    return price

# 满减券 + 打折券
def func1(m, n, k, price, num):
    # 先用满减券
    p1 = p2 = price
    p1, num1 = manjian(m, p1, num)
    p1 = dazhe(p1)
    num1 += 1
    # print("man + dazhe", p1)
    # 先用打折券
    p2 = dazhe(p2)
    p2, num2 = manjian(m, p2, num)
    num2 += 1
    # print("dazhe + man", p2)
    if(p1 < p2):
        return p1, num1
    else:
        return p2, num2
    # return min(p1, p2), num
# 满减券 + 无门槛券
def func2(m, n, k, price, num):
    p1 = p2 = price
    p1, num1 = manjian(m, p1, num)
    p1 = wumenkan(k, p1)
    num1 += k
    # print("man + wu", p1)
    p2 = wumenkan(k, p2)
    num2 = 0
    num2 += k
    p2, num2 = manjian(m, p2, num)
    # print("wu + man", p2)
    if(p1 < p2):
        return p1, num1
    else:
        return p2, num2
# 打折券 + 无门槛券
def func3(m, n, k, price, num):
    p1 = p2 = price
    p1 = dazhe(p1)
    num1 = 0
    num1 += 1
    p1 = wumenkan(k, p1)
    num1 += k
    # print("dazhe + wu", p1)
    p2 = wumenkan(k, p2)
    num2 = 0
    num2 += k
    p2 = dazhe(p2)
    num2 += 1
    # print("wu + dazhe", p2)
    if(p1 < p2):
        return p1, num1
    else:
        return p2, num2
# 满减券 + 打折券 + 无门槛券
def func4(m, n, k, price, num):
    p1, num1 = func1(m, n, k, price, num)
    p2, num2 = func2(m, n, k, price, num)
    p3, num3 = func3(m, n, k, price, num)
    if((p1 < p2) & (p1 < p3)):
        return p1, num1
    elif((p2 < p1) & (p2 < p3)):
        return p2, num2
    else:
        return p3, num3
    # return min(p1, p2, p3), num

for i in range(person):
    min_p, num = func4(m, n, k, price[i], 0)
    print(min_p, num)

# print(manjian(3,100))
# print(dazhe(100))
# print(wumenkan(3,100))
# print(func4(3, 2, 5, 100))
