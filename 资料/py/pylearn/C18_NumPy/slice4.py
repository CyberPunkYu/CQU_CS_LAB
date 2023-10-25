import numpy as np

a = np.arange(0,10,1)
print("a=\n",a)
idx = np.array([[1,3,5,7],[3,3,-3,8]])
print("idx's shape:",idx.shape)
print("idx=\n",idx)
x = a[idx]
print("x=\n",x)


