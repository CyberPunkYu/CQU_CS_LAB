import numpy as np
a = np.array([2,4,6,8])
b = np.array([1,3,5,7])

print("np.maximum(a,b)=",np.maximum(a,b))
print("a[None,:]=\n",a[None,:]) #等价于a.reshape(1,-1)
print("b[:,None]=\n",b[:,None]) #等价于b.reshape(-1,1)
print("np.maximum(a[None,:],b[:,None])\n",np.maximum(a[None,:],b[:,None]))
