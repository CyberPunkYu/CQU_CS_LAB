#poker.py
import random                                                   #导入随机数模块
suits = ["♠","♥","♦","♣"]                    #四种花色
ranks = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]  #13种牌面
#将花色与牌面组合并加上大小王，生成54张牌的列表
cards = [x+y for x in suits for y in ranks] + ["Red Joker", "Black Joker"]
#print(cards)
cardsHold = []                               #持牌列表
for i in range(17):                          #循环17次，共取17张牌
    idx = random.randint(0,len(cards)-1)     #生成一个0 到 剩余牌数-1的随机数
    c = cards.pop(idx)                       #将指定下标的牌取出
    cardsHold.append(c)                      #取出的牌添加至持牌列表

cardsHold.sort()                             #持牌列表排序
print(cardsHold)                             #打印出来看看手气