"""
Simple Peter de Jong Atrractor.
chenbo@cqu.edu.cn
程序运行有点慢，启动时请耐心等待
"""

from math import sin,cos
from matplotlib import pyplot as plt

def iteration():
    a,b,c,d = 0.970,-1.899,1.381,-1.506
    x,y = 0,0
    xdata,ydata = [],[]

    for i in range(1000000):
        xNew = sin(a*y) - cos(b*x)
        yNew = sin(c*x) - cos(d*y)
        x,y = xNew,yNew
        xdata.append(x)
        ydata.append(y)

    return xdata,ydata

xdata,ydata = iteration()
plt.figure(figsize=(6,6))
plt.title("Peter de Jong Attractor")
plt.scatter(xdata,ydata,s=0.005)
plt.show()




