import numpy as np

a = np.arange(0,50,10).reshape(-1,1)
b = np.arange(0,4)
c = a + b
print("a.shape:",a.shape,"b.shape:",b.shape,"c.shape:",c.shape)
print("a=\n",a)
print("b=",b)
print("c=\n",c)

print(b.reshape(1,-1))