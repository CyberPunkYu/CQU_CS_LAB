"""
Draw tree leaf with Iterated Function System.
chenbo@cqu.edu.cn   Dec 2018

The model was first described by Michael Barnsley.
https://en.wikipedia.org/wiki/Barnsley_fern
"""


import numpy as np
from matplotlib import pyplot as plt

def ifs(p,eq,n):
    p = np.cumsum(p)
    print(p)
    rands = np.random.rand(n)
    select = np.searchsorted(p,rands)

    result = np.zeros((n,2),dtype=np.float)
    c = np.zeros(n,dtype=np.float)

    pos = np.array([0,0,1],dtype=np.float)
    for i in range(n):
        eqidx = select[i]
        tmp = np.dot(eq[eqidx],pos)
        pos[:2] = tmp
        result[i] = tmp
        c[i] = eqidx

    return result[:,0],result[:,1],c

equations = [np.array([[0,0,0],[0,0.15,0]]),
             np.array([[0.21, -0.19, 0], [0.24, 0.27, 1.5]]),
             np.array([[-0.14, 0.26, 0], [0.26, 0.25, 0.47]]),
             np.array([[0.87, 0, 0], [-0.05, 0.84, 1.54]])]

x,y,c = ifs([0.01,0.07,0.07,0.85],equations,100000)
fig,axes = plt.subplots(1,2,figsize=(6,5))
axes[0].scatter(x,y,s=1,c='g',marker='s',linewidths=0)
axes[1].scatter(x,y,s=1,c=c,marker='s',linewidths=0)
for ax in axes:
    ax.axis("off")
plt.subplots_adjust(left=0,right=1,bottom=0,top=1,wspace=0,hspace=0)
plt.show()
