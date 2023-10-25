import numpy as np

x = np.linspace(0,10*np.pi,1000,dtype=np.float32)
y = np.zeros(1000,dtype=np.float32)
t = np.sin(x,out=y)
print(id(t),id(y))

