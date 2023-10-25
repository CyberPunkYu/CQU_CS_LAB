import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm

y,x = np.ogrid[-2:2:200j,-2:2:200j]
z = x * np.exp(-x**2-y**2)
extent = [np.min(x),np.max(x),np.min(y),np.max(y)]

plt.imshow(z,extent=extent,cmap=cm.gray)
plt.colorbar()
plt.show()



