import numpy as np
a = np.array([1,2,3])
b = np.array([3,2,1])
print(a > b)
print(a == b)
print(np.logical_or(a > b, a == b)) #等价于a >= b

print("np.all(a>b)=",np.all(a>b))
print("np.any(a>b)=",np.any(a>b))

