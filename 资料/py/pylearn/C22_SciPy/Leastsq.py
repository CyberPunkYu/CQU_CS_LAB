import numpy as np
from scipy import optimize
from matplotlib import pyplot as plt

x = np.array([4.02,6.04,8.05,10.06,12.07,13.48,15.09,17.3,20.12,24.14])
y = np.array([8.11,10.43,6.72,6.09,4.3,5.04,3.23,1.66,1.03,1.58])
def residuals(p):
    "计算以p=(k,b)为参数的直线与实验数据之间的误差"
    k,b = p
    print("try k=",k,"b=",b)
    return y - (k*x+b)

#leastsq()使得residuals()函数的输出数组的平方和为最小,[1,0]为初值
r = optimize.leastsq(residuals,[1,0])
k,b = r[0]
print("k=",k,"b=",b)

#计算y=0时的x值
print("x value when y=0:",-b/k)

plt.scatter(x,y,label="Test Points")            #画散点图
X = np.linspace(0,30,100)   #画直线图
Y = k*X + b

sLabel = "$y={:.2f}x+{:.2f}$".format(k,b)
plt.plot(X,Y,label=sLabel)
plt.legend()                #显示图示
plt.show()