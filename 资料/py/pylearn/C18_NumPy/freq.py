import numpy as np
from matplotlib import pyplot as plt

x = np.linspace(0,5*np.pi,1000)
y = np.sin(x) + 0.2*np.sin(5*x) + 0.2*np.sin(10*x)

plt.plot(x,y)
plt.show()

