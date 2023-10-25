#ndarray.py
import numpy as np

a = np.array((0,1,2,3),dtype=np.float64)
b = np.array([[0,1,2,3],[4,5,6,7]])
print("a=\n",a)
print("b=\n",b)
print("a.shape:",a.shape,"b.shape:",b.shape)
print("a.type:",type(a),"b.type:",type(b))
print("a.dtype:",a.dtype,"b.dtype:",b.dtype)
