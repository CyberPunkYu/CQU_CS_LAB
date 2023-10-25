from scipy import interpolate
import numpy as np
from matplotlib import pyplot as plt

x10 = np.linspace(0,10,10)
y10 = np.sin(x10)

plt.figure(figsize=(12,6))
ax = plt.subplot(231)
ax.scatter(x10,y10,c='black')
ax.set_title("points")

x100 = np.linspace(0,10,100)
colors = ['red','green','blue','purple']
for i,kind in enumerate(['nearest','zero','slinear','quadratic']):
    f = interpolate.interp1d(x10,y10,kind=kind)
    print("type of f:",type(f))
    y100 = f(x100)
    print(f([1,9]))
    ax = plt.subplot(232+i)
    ax.scatter(x10,y10)
    ax.plot(x100,y100,c=colors[i])
    ax.set_title(kind)

plt.subplots_adjust(left=0.05,right=0.95,bottom=0.05,top=0.95,
                    wspace=0.2,hspace=0.2)
plt.show()