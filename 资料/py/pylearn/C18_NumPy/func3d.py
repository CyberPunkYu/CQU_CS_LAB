import numpy as np
import mpl_toolkits.mplot3d
from matplotlib import pyplot as plt
from matplotlib import cm

x,y = np.mgrid[-2:2:20j,-2:2:20j]
z = x * np.exp(- x**2 - y**2)

fig = plt.figure(figsize=(8,6))
ax = fig.gca(projection='3d')
ax.plot_surface(x,y,z,cmap=cm.ocean)
plt.show()
