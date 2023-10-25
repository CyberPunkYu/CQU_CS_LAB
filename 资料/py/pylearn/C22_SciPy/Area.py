#Area.py
import numpy as np

x = np.linspace(0.7,4.0,1000)
y = np.cos(2*np.pi*x)*np.exp(-x)+1.2
dx = x[1] - x[0]                        #每个矩形的宽度
fArea = np.sum(y*dx)                    #矩形宽*高，再求和
print("Integral area:",fArea)

# print(x.shape)
# print(y.shape)
# print(dx)


