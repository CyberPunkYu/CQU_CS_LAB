import matplotlib.pyplot as plt
import numpy as np
x, y = 0.0, -1.0
x1 = x2 = x
y1 = y2 = y
step1,step2,step3 = 0.025,0.05,0.1
X, Y = [x] , [y]
X1,Y1= [x1], [y1]
X2,Y2= [x2], [y2]
def f(x:float, y:float):
    return x + y
def f2(x:float, y:float):
    return 2*x+2*x**2-2*y
#欧拉
while x < 1.0:
    k = f(x, y)
    y = y + k * step1
    x = x + step1
    X.append(x)
    Y.append(y)
#改进欧拉(欧拉中点)
k = f(x1,y1)
y = y1 + k*step2
x = x1 + step2
X1.append(x)
Y1.append(y)
i = 2
while x < 1.0:
    y = Y1[i-1]
    x = X1[i-1]
    k = f(x,y)
    y = Y1[i-2] + 2*k*step2
    x = x + step2
    X1.append(x)
    Y1.append(y)
    i += 1
#四阶RK
while x2 < 1.0:
    k1 = f(x2 , y2)
    k2 = f(x2 + 0.5*step3 , y2 + 0.5*step3*k1)
    k3 = f(x2 + 0.5*step3 , y2 + 0.5*step3*k2)
    k4 = f(x2 + step3 , y2 + step3*k3)
    y2 = y2 + step3 * (k1 + 2* k2 + 2 * k3 + k4) / 6
    x2 = x2 + step3
    Y2.append(y2)
    X2.append(x2)
testx=np.linspace(0,1,101)
testy=-1-testx
testy2=np.exp(-2*testx)+testx*testx
plt.scatter(testx,testy,s = 10 , c = 'b', label="true")
plt.scatter(X,Y,s = 10 , c = 'r',label="Euler h=0.025")
plt.scatter(X1,Y1,s = 10 , c = 'y', marker = 'v' , label="Euler_improved h=0.05")
plt.scatter(X2,Y2,s = 10 , c = 'g', marker = '*' , label="4RK h=0.1")
plt.legend()
plt.show()