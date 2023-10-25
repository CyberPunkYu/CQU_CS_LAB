import numpy as np
from numpy import random as nr

nr.seed(2018)   #相同的随机数种子使得多次运行的结果相同
a = nr.randint(0,10,size=(3,5))
print("a=\n",a)
print("np.sum(a)=",np.sum(a))
print("np.sum(a,axis=0)=",np.sum(a,axis=0))
print("np.sum(a,axis=1)=",np.sum(a,axis=1))