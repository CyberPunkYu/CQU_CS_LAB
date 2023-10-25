from numpy import random as nr
import numpy as np
from matplotlib import pyplot as plt

heights = nr.normal(170,30,(100000,)).astype(int)
stats = np.zeros((10000,))
for i in range(100000):
    stats[heights[i]] += 1

plt.plot(stats[:300])
plt.show()

