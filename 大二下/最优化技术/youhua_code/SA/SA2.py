
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
import random

#三维曲面显示
X=np.linspace(-2,2,300)
Y=np.linspace(-2,2,300)
XX, YY = np.meshgrid(X, Y)
Z=YY*np.sin(2*math.pi*XX)+XX*np.cos(2*math.pi*YY)
fig = plt.figure()
ax = Axes3D(fig)
ax.plot_surface(XX, YY, Z,rstride=1, cstride=1, cmap='rainbow')
plt.show()

#待优化(最大值)目标函数
def ObjFunc(x,y):
    return y*math.sin(2*math.pi*x)+x*math.cos(2*math.pi*y)
    
 

 
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
 


sectionl=-2
sectionh=2
xold = (sectionh-sectionl)*random.random()+sectionl
yold = (sectionh-sectionl)*random.random()+sectionl

T = 1e5
Tmin = 1e-3
alpha = 0.98
k = 50
t=0
sold=ObjFunc(xold,yold)
maxs=-999

while T>=Tmin:
    for i in range(k):        
        #generate a new x in the neighboorhood of x by transform function             
        if random.random()>0.5:
           deltax=(np.random.uniform(-1,1))*(xold-sectionl) #扰动值
           deltay=(np.random.uniform(-1,1))*(yold-sectionl)
        else:
           deltax=(np.random.uniform(-1,1))*(sectionh-xold) #扰动值
           deltay=(np.random.uniform(-1,1))*(sectionh-yold)
           
        xNew=xold+deltax # generate the new value
        yNew=yold+deltay
        if ((xNew<sectionl) or (xNew>sectionh)):
            xNew=xNew-2*deltax
        if ((yNew<sectionl) or (yNew>sectionh)):
            yNew=yNew-2*deltay
       # print(i,delta,xNew)
        sNew=ObjFunc(xNew,yNew)
        dE=sold-sNew
           
        bz=judge(dE,T)
        if bz:
            xold=xNew
            yold=yNew
            sold=sNew     
        if maxs<sNew:  # keep the minimum result during processing
            maxs=sNew
            max_coor=[xNew,yNew]
              
    t+=1
    print (t)
    # T=0.95*T #
    T=1000/(1+t) # decrease temperature
 
print(xold,yold,ObjFunc(xold,yold))
print(max_coor,maxs)