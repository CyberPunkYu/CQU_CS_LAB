import numpy as np 


def f1(x1,x2):
    return 60-10*x1-4*x2+x1**2+x2**2-x1*x2
def derivate1(x):
    return np.array([-10+2*x[0]-x[1],-4+2*x[1]-x[0]])

def derivate2():
    return np.array([[2,-1],[-1,2]])



value=[-10,10]
e=0.0001
k=0


x=np.array(value)

resultd1=derivate1(x)
resultd2=derivate2()
xx=np.matmul(resultd1,np.linalg.inv(resultd2))
print(np.linalg.inv(resultd2))
print("matrix multipy result is ",xx)
newx=x-xx
print("start...")
print('No.',str(k))
print (newx,f1(newx[0],newx[1]))
while (np.sum(abs(newx-x))>e):
    x=newx
    k=k+1
    print('No.',str(k))
    resultd1=derivate1(newx)
    newx=x-np.dot(np.linalg.inv(resultd2),resultd1)
    print (newx,f1(newx[0],newx[1]))




