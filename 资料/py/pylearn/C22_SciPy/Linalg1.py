#Linalg1.py
import numpy as np
from scipy import linalg
import timeit

n = 100
A = np.random.rand(n,n)
b = np.random.rand(n)
print("shape of A:",A.shape)
print("shape of b:",b.shape)
x = np.dot(linalg.inv(A),b)
print("x=",x)
print("shape of x:",x.shape)

print("Time cost of 100 runs:",end="\t")
print(timeit.timeit("np.dot(linalg.inv(A),b)", number=100, globals=globals()))

