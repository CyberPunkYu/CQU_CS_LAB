#利用scipy实现共轭梯度法
import numpy as np
args = (2, 3, 7, 8, 9, 10)  #原函数的参数
def f(x, *args):#原函数
    u, v = x
    a, b, c, d, e, f = args
    return a*u**2 + b*u*v + c*v**2 + d*u + e*v + f
def gradf(x, *args):
    u, v = x
    a, b, c, d, e, f = args
    gu = 2*a*u + b*v + d     # u-component of the gradient
    gv = b*u + 2*c*v + e     # v-component of the gradient
    return np.asarray((gu, gv))
x0 = np.asarray((0, 0))  # Initial guess.

#下面开始调包计算~!
from  scipy  import optimize
res1 = optimize.fmin_cg(f, x0, fprime=gradf, args=args)
print("最小值所在的向量是:",res1)
