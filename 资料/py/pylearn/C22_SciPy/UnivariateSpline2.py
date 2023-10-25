import numpy as np
from scipy import interpolate
from matplotlib import pyplot as plt

plt.figure(figsize=(12,4))
x = np.linspace(0,20,200)   #[0,20]等差数列，200个值
y = np.sin(x) + np.random.standard_normal(len(x))*0.16 #带噪声正弦
plt.scatter(x,y,s=3,label="noisy points")   #散点图：噪声实验数据点
xs = np.linspace(0,23,2000) #[0,23]等差数列，2000个值
ys = interpolate.UnivariateSpline(x,y,s=8)(xs) #由(x,y)插值，函数应用于xs
plt.plot(xs,ys,lw=2,label="spline,s=8") #画(xs,ys)，ys由插值函数计算而来
plt.plot(xs,np.sin(xs),lw=2,label="sin(x)") #画标准正弦函数(xs,np.sin(xs))
plt.legend()
plt.show()
