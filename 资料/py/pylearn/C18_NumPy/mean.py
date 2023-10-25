import numpy as np
from numpy import random as nr

nr.seed(2018)   #相同的随机数种子使得多次运行的结果相同
a = nr.randint(0,10,size=(3,5))
print("a=\n",a)
print("np.mean(a,axis=1)=",np.mean(a,axis=1))

score = np.array([66,77,88])
weights = np.array([0.3,0.5,0.2])
print("np.average():",np.average(score,weights=weights))

