import numpy as np

a = np.arange(0,10,1)
print("a=",a)
x = a[[1,3,5,7]]
x[1] = 77
x[[2,3]] = 88,99
print("x=",x)
y = a[[3,3,-3,8]]
print("y=",y)
print("a=",a)

