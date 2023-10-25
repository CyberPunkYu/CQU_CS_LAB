import math
def  firstDerivative(x):
    return 4*(x**3-3*(x**2)-3*x-4)
def secondDerivative(x):
    return  12*(x**2-2*x-1)

def newtonmethod(a0,eps):
   while 1:
     firstD=firstDerivative(a0)
     secondD=secondDerivative(a0)
     a1=a0-firstD/secondD
     print(a1)
     if math.fabs(a1-a0)<eps:
         break
     a0=a1
   return a1
print("the mimum value is :",newtonmethod(3,0.001))