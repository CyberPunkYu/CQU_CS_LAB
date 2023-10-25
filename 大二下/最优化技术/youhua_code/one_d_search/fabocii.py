import matplotlib.pyplot as plt
import numpy as np
import math
def  calFunc(x):
  return 2*(x**2)-2*x-1#-x*(350-2*x)*(260-2*x)  #2*(x**2)-7*x-1


def fabonacci(n):
    n=n+1
    if n>=0:
        a=(1+math.sqrt(5))/2
        b=(1-math.sqrt(5))/2
        c=a**n-b**n
        return c/math.sqrt(5)

def fibonacci_method(a,b,e):
    # calculate n
    n=0
    while fabonacci(n)<(b-a)/e:
        n=n+1

    x1=a+fabonacci(n-2)/fabonacci(n)*(b-a)
    x2=a+fabonacci(n-1)/fabonacci(n)*(b-a)
    f1=calFunc(x1)
    f2=calFunc(x2)
    for i in range(1,n-1):
        if f1<f2:
            b=x2
            x2=x1
            f2=f1
            x1=a+fabonacci(n-2-i)/fabonacci(n)*(b-a)
            f1=calFunc(x1)
            print("zeros is [{},{}]".format(a,b))
        else:
            a=x1
            x1=x2
            f1=f2
            x2=a+fabonacci(n-1-i)/fabonacci(n)*(b-a)
            f2=calFunc(x2)
            print("zeros is [{},{}]".format(a,b))
    if f1<f2:
        b=x2
        print("zeros is [{},{}]".format(a,b))
    else:
        a=x1
        print("zeros is [{},{}]".format(a,b))
    return         

fibonacci_method(0,0.6,0.16)

plt.figure(1)
x=np.linspace(-0,1,10)
plt.plot(x,calFunc(x))
plt.show()


