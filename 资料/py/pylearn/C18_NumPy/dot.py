import numpy as np
from numpy import random as nr

nr.seed(2018)
a = nr.randint(0,5,(2,3))
print("a=\n",a)
b = nr.randint(0,5,(3,2))
print("b=\n",b)
c = np.dot(a,b)
print("c=a*b=\n",c)

