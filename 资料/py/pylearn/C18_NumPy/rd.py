from numpy import random as nr

r1 = nr.rand(3,2)   #0-1的随机数，3,2表示形状
r2 = nr.randn(3,2)  #标准正态分布的随机数
r3 = nr.randint(0,10,(3,2)) #0-9(不含10)的随机数
print(r1)
print(r2)
print(r3)