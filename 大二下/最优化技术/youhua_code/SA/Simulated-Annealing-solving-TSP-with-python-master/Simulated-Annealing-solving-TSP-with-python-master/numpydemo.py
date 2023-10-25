import numpy as np
A = np.array([1,2,3,4])
print(A)
print(np.ndim(A))  # 输出维度
print(A.shape)     # 输出形状
print(A.shape[0])
x=np.array([[2,-1],[-1,2]])
invx=np.linalg.inv(x)
print(x)
print(invx)