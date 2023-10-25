#Quad.py
import math
from scipy import integrate

def func(x):
    print("x=",x)       #用于展示quad()函数对func的多次调用
    return math.cos(2*math.pi*x)*math.exp(-x)+1.2

fArea,err = integrate.quad(func,0.7,4)
print("Integral area:",fArea)

