import numpy as np
a = np.arange(10)
print("a=",a)
print("a[2]=",a[2])
print("a[1:3]=",a[1:3])
print("a[-1::-1]=",a[-1::-1])
print("a[:-5]=",a[:-5])
a[:3] = 77,88,99
print("a=",a)
