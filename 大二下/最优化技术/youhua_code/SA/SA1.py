
import numpy as np
import matplotlib.pyplot as plt
import math


#define aim function
def aimFunction(x):
    y= x*math.sin(x) #x**3-60*x**2-4*x+6#
    return y

sectionl=-4
sectionh=16

def judge(dE,tmp): #metropolis principle
    if dE<0:
       return 1
    else:
        p=math.exp(-(dE/tmp))
        r=np.random.uniform(low=0,high=1)
        if p>r:
           return 1
        else:
           return 0


x=[((sectionh-sectionl)*(i/100)+sectionl) for i in range(100)]
y=[0 for i in range(100)]
for i in range(100):
    y[i]=aimFunction(x[i])

plt.figure()
plt.ion()
plt.cla()
plt.plot(x,y)
plt.pause(0.1)


T=1000 #initiate temperature
Tmin=0.1 #minimum value of terperature

xold=np.random.uniform(low=sectionl,high=sectionh)#initiate x

k=100 #times of internal circulation 
yold=0#initiate result
t=0#time
miny=100 # minimum result
minx=0  # 
yold=aimFunction(xold)  #calculate y
xNew=0
yNew=0
while T>=Tmin:
    for i in range(k):        
        #generate a new x in the neighboorhood of x by transform function             
        delta=(np.random.uniform(-0.005,0.005))*T #扰动值
        # delta=(np.random.uniform(0,1)-0.5)*5
        xNew=xold+delta # generate the new value
       # print(i,delta,xNew)

        if ((xNew<sectionl) or (xNew>sectionh)):
            xNew=xNew-2*delta
        else:
           yNew=aimFunction(xNew)
           dE=yNew-yold
           
           bz=judge(dE,T)
           if bz:
              xold=xNew
              yold=yNew     
              if miny>yNew:  # keep the minimum result during processing
                  miny=yNew
                  minx=xNew
              #draw point
              plt.cla()
              plt.plot(x,y)
              plt.plot(xold,yold,'+r')
              plt.pause(0.1)
    t+=1
    print (t)
    # T=0.95*T #
    T=1000/(1+t) # decrease temperature

#x=minx
print (xNew,aimFunction(xNew))
print(minx,miny)


plt.ioff()
plt.plot(xold,yold,'.r')
plt.plot(minx,miny,'*b')
plt.show()

