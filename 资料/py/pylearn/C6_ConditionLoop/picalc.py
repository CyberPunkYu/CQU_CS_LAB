#picalc.py
import random                   #随机数模块
N,nHits = 10000,0               #总投点数，圆内投点数
xs,ys = [],[]                   #投点的x,y坐标列表

for i in range(N):              #N次投点
     x = random.random()*2-1    #随机数取投点坐标
     y = random.random()*2-1
     xs.append(x)               #投点坐标存入列表
     ys.append(y)
     if x*x+y*y <= 1:           #投点位于内切圆内
         nHits += 1             #圆内投点数 + 1

pi = 4*nHits/N                  #通过计算圆面积估算圆周率
print("pi =",pi)

import matplotlib.pyplot as plt    #绘图展现投点落在正方形/圆内的情况
from matplotlib.patches import Circle
fig = plt.figure(figsize=(6,6))
plt.plot(xs, ys,'o', color='black', markersize = 1)
c = Circle(xy=(0,0), radius=1, alpha=0.4, color="black")
plt.gca().add_patch(c)
plt.show()


