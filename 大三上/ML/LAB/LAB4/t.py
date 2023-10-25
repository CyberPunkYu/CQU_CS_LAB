import numpy as np
def beale(x1,x2):
    return (1.5-x1+x1*x2)**2+(2.25-x1+x1*x2**2)**2+(2.625-x1+x1*x2**3)**2

#定义beale公式的偏导函数
def dbeale(x1, x2):
    dfdx1 = 2*(1.5-x1+x1*x2)*(x2-1)+2*(2.25-x1+x1*x2**2)*(x2**2-1)+2*(2.625-x1+x1*x2**3)*(x2**3-1) # 求beale公式关于x1的偏导数
    dfdx2 = 2*(1.5-x1+x1*x2)*x1+2*(2.25-x1+x1*x2**2)*(2*x1*x2)+2*(2.625-x1+x1*x2**3)*(3*x1*x2**2) # 求beale公式关于x2的偏导数
    return dfdx1, dfdx2


a = np.array((3,1))
r = np.zeros((2, ))
r += a**2
b = 0
b += a**2
print(b)
b=np.sqrt(b)
print(b)
r = np.sqrt(r)
print(r)
# print(beale(0.12036067670871019, -0.0032866317506335244))
# print(dbeale(0.12036067670871019, -0.0032866317506335244))