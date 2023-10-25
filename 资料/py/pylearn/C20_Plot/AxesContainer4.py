from matplotlib import pyplot as plt
import numpy as np
fig = plt.figure()
ax = fig.add_subplot(111)
c = ax.scatter(np.random.rand(20),np.random.rand(20))   #随机散点图
print("type(c):",type(c))
print("c in ax.collections:",c in ax.collections)
plt.show()