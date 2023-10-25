import numpy as np

a = [[x+y*10 for x in range(5)] for y in range(6)]
a = np.array(a).astype(int)

print("a[(0,1,1,3),(1,2,2,4)]=",a[(0,1,1,3),(1,2,2,4)])
print("a[4:,[0,2,4]]=\n",a[4:,[0,2,4]])
select = np.array([0,1,0,0,1,1],dtype=np.bool)
print("a[select,1]=",a[select,1])
