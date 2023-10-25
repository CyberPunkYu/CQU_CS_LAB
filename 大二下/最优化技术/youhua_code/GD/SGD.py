import numpy as np

x0=np.random.randint(1,2,100).reshape(100,1)
x1=np.random.randint(1,10,100).reshape(100,1)
y=x0+x1
X=np.hstack((x0,x1))

def SGD(X,y):
    ept = 0.001  #精度
    loss = 1     #损失
    alpha = 0.01 #学习率
    max_iter = 0 #迭代次数
    theta = np.random.randint(1,10,(X.shape[1],1)) #初始化
    numsSample = X.shape[0]
    while max_iter <= 10000 or loss < ept:
        i = np.random.randint(0, numsSample) #随机抽取一个样本
        partial=X[i:i+1,:].T.dot((X[i:i+1,:].dot(theta)-y[i,:]).reshape(1,1)) #损失函数关于theta的偏导数
        theta=theta-alpha*partial
        max_iter+=1
        loss=(1/(2*X.shape[0]))*np.sum((X.dot(theta)-y)**2)
    return max_iter,theta
