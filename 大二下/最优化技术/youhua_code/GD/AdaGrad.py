import numpy as np
import math
x0=np.random.randint(1,2,100).reshape(100,1)
x1=np.random.randint(1,10,100).reshape(100,1)
y=x0+x1
x=np.hstack((x0,x1))

#多元线性回归  y = x0 + x1, X = [x0 , x1]
def AdaGrad(x,y):
    m, dim = x.shape
    theta = np.zeros(dim) 
    alpha = 0.01
    ept = 0.0001
    loss = 0
    e = 0.00000001
    b2 = 0.999
    mt = np.zeros(dim)
    vt = np.zeros(dim)
    max_iter = 0
    while max_iter <= 10000 or loss < ept:
        j = max_iter % m
        loss = 1 / (2 * m) * np.dot((np.dot(x, theta) - y).T , (np.dot(x, theta) - y))
        gradient = x[j] * (np.dot(x[j] , theta) - y[j])
        vt = b2 * vt + (1 - b2) * (gradient**2)
        vtt = vt / (1 - (b2**(i + 1)))
        vtt_sqrt = np.array([math.sqrt(vtt[0]),
                             math.sqrt(vtt[1])])  # 因为只能对标量进行开方
        theta = theta - alpha * gradient / (vtt_sqrt + e)