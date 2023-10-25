
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import pyplot as plt
 
fig = plt.figure()
ax = Axes3D(fig)
x=np.arange(-2*np.pi,2*np.pi,0.1)
y=np.arange(-2*np.pi,2*np.pi,0.1)
X, Y = np.meshgrid(x, y)#网格的创建，这个是关键
Z=np.sin(X)*np.cos(Y)
plt.xlabel('x')
plt.ylabel('y')
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='rainbow')
plt.show()

