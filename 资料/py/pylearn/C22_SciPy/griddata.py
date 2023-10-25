import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
from scipy import interpolate
from scipy import misc
import matplotlib
import cv2  #请张浩确认IMAGE 2.1上有安装这个opencv2的包，如果无，需要考虑其它存储方案

x,y,z = [],[],[]   #三个输入列表
#随便加入一些离散点 
x.append(0)    #横    
y.append(0)    #纵坐标
z.append(120)   #dB值, 简单起见，提前把dB映射到0-255

x.append(600)
y.append(600)
z.append(140)

x.append(0)
y.append(600)
z.append(20)

x.append(300)
y.append(300)
z.append(200)

x.append(600)
y.append(0)
z.append(125)

print("interpolate start...")
#假设图像为NxN像素
N = 600
xo = np.linspace(0,N,N) + np.zeros(N).reshape(-1,1)
yo = np.linspace(0,N,N).reshape(-1,1) + np.zeros(N)
xyo = np.c_[xo.ravel(), yo.ravel()]

print("xo.shape",xo.shape)
print("yo.shape",yo.shape)
print("xyo.shape",xyo.shape)

#cubic,  linear, nearest三个值都尝试一下看哪个合适, 
zo = interpolate.griddata((x,y),z,xyo,method="cubic").reshape(N,N)
zo[0][0] = 255   #特殊处理，让matplotlib以及opencv2都可以正确处理灰度， 255为白，0为黑
zo[0][1] = 0
print(zo.shape)

print("interpolate end")

cv2.imwrite("zo.jpg",zo)   #存图方案1，需要确认IMAGE 2.1卡上有没有CV2包
matplotlib.image.imsave("zo.png",zo,cmap=cm.gray) #存图方案2  根据测试结果选择

print("save file end")

plt.figure(figsize=(4,4))
extent = [np.min(xo),np.max(xo),np.min(yo),np.max(yo)]
ax = plt.subplot(111)
ax.imshow(zo,extent=extent,cmap=cm.gray)
ax.set_title("600x600")

plt.show()


