import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
from scipy import interpolate

plt.figure(figsize=(12,4))

y,x = np.ogrid[-2:2:20j,-2:2:20j]
z = (x+y)*np.exp(-x**2-y**2)    #20x20的实验数据点
extent = [np.min(x),np.max(x),np.min(y),np.max(y)]
ax = plt.subplot(131)
ax.imshow(z,extent=extent,cmap=cm.rainbow)
ax.set_title("20x20")

print(x.shape, y.shape, z.shape)
func = interpolate.interp2d(x,y,z,kind='cubic') #二维插值
x1 = np.linspace(-2,2,300)
y1 = np.linspace(-2,2,300)
z1 = func(x1,y1)    #根据插值函数计算函数值，要求参数为一维数组
ax = plt.subplot(132)
ax.imshow(z1,extent=extent,cmap=cm.rainbow)
ax.set_title("interp2d_300x300")

y2,x2 = np.ogrid[-2:2:300j,-2:2:300j]
z2 = (x2+y2)*np.exp(-x2**2-y2**2)   #计算标准函数并显示以便对照
ax = plt.subplot(133)
ax.imshow(z2,extent=extent,cmap=cm.rainbow)
ax.set_title("original_300x300")

plt.show()