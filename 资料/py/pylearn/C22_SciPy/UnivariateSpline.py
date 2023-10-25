import numpy as np
from scipy import interpolate
from matplotlib import pyplot as plt

plt.figure(figsize=(12,4))
x = np.linspace(0,10,20)    #[0,10]含20个值的等差数列
y = np.sin(x)               #y = x的正弦
plt.scatter(x,y,s=20,label="points")   #画散点图
xs = np.linspace(0,12,100)             #[0,12]含100个值的等差数列，12>10,外推
ys = interpolate.UnivariateSpline(x,y,s=0)(xs)  #由(x,y)插值，函数应用于xs
plt.plot(xs,ys,lw=2,label="spline,s=0")   #画(xs,ys)，ys由插值函数计算而来
plt.plot(xs,np.sin(xs),lw=2,label="sin(x)") #画标准正弦函数(xs,np.sin(xs))
plt.legend()    #显示图示
plt.show()



