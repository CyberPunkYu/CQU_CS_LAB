import numpy as np
import matplotlib.pyplot as plt

r = np.arange(0, 2, 0.01)
theta = 2 * np.pi * r
ax = plt.subplot(111, projection='polar')
ax.plot(theta,r,color="r",lw=3)
ax.set_rmax(2)
ax.set_rticks([0.5, 1, 1.5, 2])  #减少r向刻度
ax.set_rlabel_position(250)  #设置r向刻度标签至250度方向
ax.grid(True)
ax.set_title("A line plot on a polar axis", va='bottom')
plt.show()