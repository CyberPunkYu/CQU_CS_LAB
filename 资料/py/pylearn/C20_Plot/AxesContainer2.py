from matplotlib import pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111)
n,bins,rects = ax.hist(np.random.randn(1000),50,facecolor='g')
print("len(rects):",len(rects),"len(ax.patches):",len(ax.patches))
print(rects[0] is ax.patches[0])
print(type(ax.patches[0]))
plt.show()