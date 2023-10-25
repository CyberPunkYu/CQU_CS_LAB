import numpy as np

a = np.arange(0,5,1)
idx1 = [True,False,False,True,False]
print("a[idx1]=",a[idx1])

idx2 = (a % 2 == 0)
print("idx2=",idx2)
print("a[idx2]=",a[idx2])

print(a[a%2==0])

