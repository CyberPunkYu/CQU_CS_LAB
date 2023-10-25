import matplotlib.pyplot as plt
from matplotlib.collections import EllipseCollection, RegularPolyCollection
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111)

angles = np.linspace(0,2*np.pi,10,endpoint=False)  #0-2π, 等分10份作为旋转角 (10,)
pos1 = np.c_[4*np.cos(angles),2*np.sin(angles)]    #椭圆集合的绘图位置     (10,2)
pos2 = np.c_[1.5*np.cos(angles),.8*np.sin(angles)] #正多边形集合的绘图位置 (10,2)
angles = np.rad2deg(angles) #将0-2π的弧度单位转换至0-360度的角度单位

ec = EllipseCollection([2]*10,[1]*10,angles,units='x', offsets=pos1,
                       array=angles,cmap=plt.cm.rainbow,transOffset=ax.transData)
ax.add_collection(ec)

pc = RegularPolyCollection(7,sizes=(200,)*10,offsets=pos2,array=angles,
                           cmap=plt.cm.rainbow,transOffset=ax.transData)
ax.add_collection(pc)
ax.axis((-6,6,-5,5))
plt.colorbar(pc,ax=ax)

plt.show()