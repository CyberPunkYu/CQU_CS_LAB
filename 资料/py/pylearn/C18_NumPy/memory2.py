import numpy as np
a = np.array([[1,2,3],[4,5,6],[7,8,9]],dtype=np.float32)
b = a[::2,::2]
print("a=\n",a)
print("b=\n",b)
print("a.strides=",a.strides)
print("b.strides=",b.strides)
print("a.data=",a.data)
print("b.data=",b.data)

