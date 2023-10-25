import math
import numpy as np
from matplotlib import pyplot as plt

def signalcomp(x,freq):
    y = math.cos(x)
    y += 0.2*math.cos(freq*x)
    return y

x = np.linspace(0,5*np.pi,1000)
ufunc1 = np.frompyfunc(signalcomp,2,1)
y = ufunc1(x,10).astype(np.float32)

plt.plot(x,y)
plt.show()

