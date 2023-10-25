import numpy as np

x,y = np.ogrid[0:3:4j,0:4:5j]
print("x=\n",x)
print("y=\n",y)
print("x.shape=",x.shape)
print("y.shape=",y.shape)