import numpy as np
from numpy import random as nr
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig = plt.figure(figsize=(6, 6))
ax = fig.add_axes([0, 0, 1, 1])  #添加子图ax覆盖整个fig
ax.set_xlim(0, 1), ax.set_xticks([])  #横纵坐标的范围均为[0-1],不显示刻度
ax.set_ylim(0, 1), ax.set_yticks([])

nDrops = 60 #雨滴总数
xyDrops = np.random.uniform(0,1,(nDrops,2)) #雨滴位置


sizeDrops = np.zeros(nDrops)                #雨滴尺寸
colorDrops = np.zeros((nDrops,4))           #雨滴颜色
print(sizeDrops.shape)
growthDrops = np.random.uniform(20,200,nDrops)  #雨滴尺寸增长率
scatterDrops = ax.scatter(xyDrops[:, 0], xyDrops[:, 1],s=sizeDrops, lw=2, #散点图 
               	edgecolors=colorDrops,facecolors='none')  #返回类型PathCollection

def update(frameNumber):    #每次update()函数被调用执行，frameNumber会自动加1
    colorDrops[:, 3] -= 1.0/nDrops  #逐渐增加雨滴透明度
    colorDrops[:, 3] = np.clip(colorDrops[:, 3], 0, 1)  #限定透明度值在[0,1]范围内
    global sizeDrops
    sizeDrops += growthDrops  #按增长率增加雨滴尺寸，让雨滴变大

    idx = frameNumber % nDrops                  #求模找出最“老”雨滴的下标idx
    xyDrops[idx] = np.random.uniform(0,1,2)     #将最“老”雨滴移至随机位置
    sizeDrops[idx] = 0                          #将最“老”雨滴变小
    colorDrops[idx] = (nr.rand(), nr.rand(), nr.rand(), 1) #给最“老”雨滴置随机颜色
    growthDrops[idx] = np.random.uniform(20, 200)   #给最“老”雨滴一个随机增长率

    scatterDrops.set_edgecolors(colorDrops)  #重新设置散点图各对象边线颜色
    scatterDrops.set_sizes(sizeDrops)        #重新设置散点图各对象尺寸
    scatterDrops.set_offsets(xyDrops)        #重新设置散点图各对象偏移量，即位置
    print("frameNumber:",frameNumber,"oldest drop renewed:",idx)


ani = FuncAnimation(fig, update, interval=10) #为fig创建动画，每10ms执行一次update函数
plt.show()
