import numpy as np
from matplotlib import pyplot as plt

x = np.linspace(0,6,1000)
y = np.cos(2*np.pi*x)*np.exp(-x)+1.2        #输出值应为2.2
print("np.max(y):",np.max(y))

fig,ax = plt.subplots(figsize=(10,5))
ax.plot(x,y,label="$cos(2πx)e^{-x}+1.2$")      #画曲线，带图示
ax.axis([np.min(x),np.max(x),0,np.max(y)])     #坐标范围
ax.fill_between(x,y1=y,y2=0,where=(x>=0.7)&(x<=4),   #填充积分区域
                  facecolor='blue',alpha=0.2)
plt.legend()       #显示图示

print(type(ax.transData))
print("ax.transData.transform([(0,0),(3,1.1),(6,2.2)])=")
print(ax.transData.transform([(0,0),(3,1.1),(6,2.2)]))

print(type(ax.transAxes))
print(ax.transAxes.transform([(0,0),(0.5,0.5),(1,1)]))

print(type(fig.transFigure))
print(fig.transFigure.transform([(0,0),(0.5,0.5),(1,1)]))

print("ax.transData.transform([(0,0),(3,1.1),(6,2.2)])=")
print(ax.transData.transform([(0,0),(3,1.1),(6,2.2)]))

transDataInverted = ax.transData.inverted()
print(transDataInverted.transform((320,200)))

plt.show()
