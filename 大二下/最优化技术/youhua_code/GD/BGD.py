import numpy as np

x0=np.random.randint(1,2,100).reshape(100,1) #x0全为1
x1=np.random.randint(1,10,100).reshape(100,1)
y=x0+x1
X=np.hstack((x0,x1))

print(y)
print(y.shape[0],y.shape[1])
print(X)
print(X.shape[0],X.shape[1])
def BGD(X,y):
    ept = 0.001  #精度
    loss = 1     #定义一个损失 方便进入循环体 后来表示两次迭代损失函数的差异
    alpha = 0.01 #学习率
    max_iter = 0 #迭代次数
    theta = np.random.randint(1,10,(X.shape[1],1)) #初始化
    while max_iter <= 10000 or loss < ept:
        partial = (1/X.shape[0])*X.T.dot(X.dot(theta)-y) #损失函数关于theta的偏导数
        theta=theta-alpha*partial
        max_iter+=1
        loss=(1/(2*X.shape[0]))*np.sum((X.dot(theta)-y)**2) #计算两次迭代之间的差异(损失函数) 无明显差异就说明算法收敛到了全局最优解
    return max_iter,theta
 
