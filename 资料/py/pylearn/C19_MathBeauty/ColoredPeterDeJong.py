"""
Colored Peter de Jong Atrractor.
chenbo@cqu.edu.cn   Dec 2018
"""

from math import sin,cos
from matplotlib import pyplot as plt

def iteration():
    e,f = 0.7,-1.1
    # a,b,c,d = 0.970,-1.899,1.381,-1.506
    # a,b,c,d = -0.709,1.638,0.452,1.740
    # a,b,c,d = 1.641,1.902,0.316,1.525
    # a,b,c,d = 1.4,-2.3,2.4,-2.1
    a,b,c,d = 2.01,-2.53,1.61,-0.33
    x,y,z = 0,0,0

    xdata,ydata,zdata = [],[],[]
    for i in range(1000000):
        xNew = sin(a*y) - cos(b*x)
        yNew = sin(c*x) - cos(d*y)
        zNew = sin(e * x) - cos(f * z)

        x,y,z = xNew,yNew,zNew
        xdata.append(x)
        ydata.append(y)
        zdata.append(z)

    return xdata,ydata,zdata

xdata,ydata,zdata = iteration()
plt.figure(figsize=(6,6))
plt.title("Peter de Jong Attractor")
plt.scatter(xdata,ydata,s=0.005,c=zdata)
plt.show()




