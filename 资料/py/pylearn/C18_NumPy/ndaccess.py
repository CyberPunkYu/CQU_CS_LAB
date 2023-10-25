import numpy as np

a = [[x+y for x in range(5)] for y in range(6)]
a = np.array(a).astype(int)
print("a[1,2:4]=",a[1,2:4])
print("a[4:,3:]=\n",a[4:,3:])
print("a[:,1]=\n",a[:,1])
print("a[0::3,::2]=\n",a[0::3,::2])




# print(a[3][2])
# print(a[3,2])
# idx = (3,2)
# print(a[idx])


