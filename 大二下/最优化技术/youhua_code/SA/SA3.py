# using SA algorithm (classical algorithm)
import numpy as np
import matplotlib.pyplot as plt
import math
import random


#define aim function
def Cal_distance(city):# Calculate the distance between cities
    d=0
    for i in range(city.shape[0]-1):
       d+=math.sqrt(np.sum(np.power(city[i+1,:]-city[i,:],2)))
    d+=np.sum(np.power(city[i+1,:]-city[0,:],2))
    return d


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



#initiate x
# xold=np.array([[41,94],[37,84],[54,67],[25,62],[7,64],[2,99],[68,58],[71,44],[54,62],[83,69],[64,60],[18,54],[22,60],[83,46],[91,38],[25,38],[24,42],[58,69],[71,71],[74,78],[87,76],[18,40],[13,40],[82,7],[62,32],[58,35],[45,21],[41,26],[44,35],[4,50]])
# xold=np.array([[0,0],[1,10],[2,8],[9,5],[1.3,5],[7,9],[3,3],[6,4],[9,8],[8.1,6.8],[15,16],[12.5,18.6],[14.8,18.4],[2.3,15.7],[9.1,19]])
xold=np.array([[0,0],[3,3],[6,4],[9,5],[8.1,6.8],[9,8],[15,16],[14.8,18.4],[12.5,18.6],[9.1,19],[7,9],[2.3,15.7],[1,10],[2,8],[1.3,5]])
city_coor=xold


city_num=xold.shape[0]
T=100*city_num #initiate temperature
Tmin=0.001 #minimum value of terperature
def generate(cities):
    # while 1:
    #   p1=random.randint(0,city_num-1)
    #   p2=random.randint(0,city_num-1)
    p1,p2=random.sample(range(city_num),2)

    #   if p1!=p2:
    #       break

    cities[[p1,p2],:]=cities[[p2,p1],:]
    # np.random.shuffle(cities)
    
    return cities


k=100 #times of internal circulation 
t=0#time
mind=1e+5 # minimum result

dold=Cal_distance(xold)  #calculate y
costall=[dold]
plt.ion()
while T>=Tmin and t<100000:
    for i in range(k):        
        #generate a new x in the neighboorhood of x by transform function             
        xNew=generate(xold)
       # print(i,delta,xNew)

        dNew=Cal_distance(xNew)# calculate the distance in new route
        dE=dNew-dold
           
        bz=judge(dE,T)
        if bz:
            xold=xNew
            dold=dNew   
            # plt.cla()
            # plt.plot(xold[:,0],xold[:,1],'g')
            # plt.pause(0.1)

            if mind>dNew:  # keep the minimum result during processing
                mind=dNew
                minx=xNew
                plt.cla()
                plt.plot(minx[:,0],minx[:,1],'b')
                plt.pause(0.1)

    
    costall.append(dold)  
    t+=1
    print (t)

    # T=0.99*T #
    T=1000/(1+t) # decrease temperature

#x=minx
print(mind)
plt.ioff()
newcost=enumerate(costall)

plt.plot(city_coor[:,0],city_coor[:,1],'ro')
plt.figure()
plt.plot(costall)


plt.show()


