import numpy as np
from numpy import random as nr

nr.seed(2018)   #相同的随机数种子使得多次运行的结果相同
a = nr.randint(0,10,size=(3,5))
print("a=\n",a)
print("np.sort(a,axis=None)=",np.sort(a,axis=None))
print("np.sort(a,axis=1)=\n",np.sort(a,axis=1))
print("np.argsort(a,axis=1)=\n",np.argsort(a,axis=1))
