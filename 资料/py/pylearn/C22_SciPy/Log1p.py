#Log1p.py
import math
import scipy.special as S
v1 = 1.0 + 1e-25
print("v1=",v1, "   #1.0 + 1e-25")
print("math.log(v1)=",math.log(v1))
v2 = 1e-25
print("v2=",v2)
print("S.log1p(v2)=",S.log1p(v2))

