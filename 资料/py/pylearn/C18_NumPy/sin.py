import numpy as np
from matplotlib import pyplot as plt

x = np.linspace(0,10*np.pi,1000)
y = np.sin(x)
print("x.shape:",x.shape,"y.shape:",y.shape)
print("x[0::100]=",x[0::100])
print("y[0::100]=",y[0::100])
plt.plot(x,y)
plt.show()