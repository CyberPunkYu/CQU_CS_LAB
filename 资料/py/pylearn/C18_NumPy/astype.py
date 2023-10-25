import numpy as np

b = np.array([[0,1,2,3],[4,5,6,7]])
a = b.reshape((4,2))       #a,b共享内存
b[1][2] = 9999
c = a.astype(np.complex)   #c与a相互独立，内存不共享
a[3][1] = 8888
print(c)

