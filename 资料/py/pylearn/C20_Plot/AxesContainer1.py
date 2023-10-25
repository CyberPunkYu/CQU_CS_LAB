from matplotlib import pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111)
ax.patch.set_color('gray')
ax.patch.set_alpha(0.2)
lines1 = ax.plot([0,1,2],[0,1,0],[0,1,2],[1,0,1]) #返回一个Line2D列表
plt.show()