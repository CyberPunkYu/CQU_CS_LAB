import numpy as np
from matplotlib import pyplot as plt

x = np.linspace(0,6,1000)
y = np.cos(2*np.pi*x)*np.exp(-x)+1.2        #输出值应为2.2
print("np.max(y):",np.max(y))
print(np.min(y))

fig,ax = plt.subplots(figsize=(10,5))
ax.plot(x,y,label="$cos(2πx)e^{-x}+1.2$")      #画曲线，带图示
ax.axis([np.min(x),np.max(x),0,np.max(y)])     #坐标范围
ax.fill_between(x,y1=y,y2=0,where=(x>=0.7)&(x<=4),   #填充积分区域
                  facecolor='blue',alpha=0.2)

plt.legend()       											#显示图示

plt.rcParams["font.family"] = "SimHei"          			#支持中文显示
ax.text(0.5*(0.7+4),0.5,r"$\int_{0.7}^4(cos(2πx)e^{-x}+1.2)\mathrm{d}x$",
        transform=ax.transData,horizontalalignment='center',#$$包含LaTex公式
        verticalalignment='center',fontsize=14)         	#公式文本

ax.text(0.05,0.95,"定积分示例",transform=ax.transAxes,
        verticalalignment='top',fontsize=14,
        bbox={"facecolor":"red","alpha":0.4,"pad":10})

xCord,yCord = 0.7,np.cos(2*np.pi*0.7)*np.exp(-0.7)+1.2     	#x=0.7时的x,y值对
ax.plot(xCord,yCord,"o")                        	        #画圆点

ax.annotate("({:.1f},{:.2f})".format(xCord,yCord),          #添加箭头注释
            xy=(xCord,yCord),xycoords="data",
            xytext=(0.4,0.8),textcoords="axes fraction",
            fontsize=14,arrowprops={"arrowstyle":"->"})

plt.show()