import numpy as np
import matplotlib.pyplot as plt

y,x = np.ogrid[-2:2:200j,-2:2:200j] #生成形状为(200,1)和(1,200)的广播数组
z = x * np.exp(-x**2-y**2)  #计算定义在x,y上的函数z,过程中有广播运算 
extent = [np.min(x),np.max(x),np.min(y),np.max(y)] #x,y的取值范围

fig, ax = plt.subplots()
c = ax.contour(z,levels=10,extent=extent) #绘制z的等值线图，z的形状为(200,200)
print(type(c))
ax.clabel(c, inline=1, fontsize=10)
ax.set_title('$z = xe^{-x^2-y^2}$')
plt.show()
