import numpy as np

a = np.arange(10)
b = a[1:5]
b[3] = 99
c = a[::2]
c[1] = 88
print(a)