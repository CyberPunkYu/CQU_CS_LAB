import numpy as np
a = np.arange(6,dtype=np.float32).reshape(2,3)
print(a[1,2],type(a[1,2]))
print(a.item(1,2),type(a.item(1,2)))
