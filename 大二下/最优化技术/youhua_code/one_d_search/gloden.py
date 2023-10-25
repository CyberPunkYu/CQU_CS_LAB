
import matplotlib.pyplot as plt
import numpy as np
def  calFunc(x):
  return 2*(x**2)-2*x-1#x**2-7*x+10#-x*(350-2*x)*(260-2*x)  #2*(x**2)-7*x-1

def searchinterval(x0,h):
# searchInterval
# Input:
#       x0:initial  point;
#       h:step;
#       
# Output:
#        [a,b]: interval;

    x1=x0
    f1=calFunc(x1)
    x2=x1+h
    f2=calFunc(x2)
    while f1>f2:
        x3=x2+h
        f3=calFunc(x3)
        if f3>f2:
            return [x1,x3]
        else:
            h=2*h
            x1=x2      
            x2=x3
            f1=calFunc(x1)
            f2=calFunc(x2)
    
    while f1<f2:
        x1,x2=x2,x1
        f1,f2=f2,f1
        h=-h
        x3=x2+h
        f3=calFunc(x3)
        if f3>f2:
            return [x1,x3]
        else:
            h=2*h
            x1=x2      
            x2=x3
            f1=calFunc(x1)
            f2=calFunc(x2)

[a,b]=searchinterval(-50,1)  
print(a,b)    

def golden(a,b,ep):
# golden section method
# input:
# [a,b]: interval 
# ep:threshold
# output：minimum value   
   while 1:
    if b-a<=ep:
        m=(a+b)/2
        #print("x=", (a+b)/2)
        return a,b,m
    a1=a+0.382*(b-a)
    a2=a+0.618*(b-a)
    f1=calFunc(a1)
    f2=calFunc(a2)
    
    if f1>f2:       
        a=a1

    else:       
        b=a2
ep=0.15
'''a=-0.5
b=0.5'''
[xmin,xmax,xmedian]=golden(a,b,ep)
print("[{},{}],xmedian={}".format(xmin,xmax,xmedian))

plt.figure(1)
x=np.linspace(-100,130,130)
plt.plot(x,calFunc(x))
plt.show()