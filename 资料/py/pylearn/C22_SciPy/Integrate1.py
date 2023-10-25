#integrate1.py
import numpy as np
from matplotlib import pyplot as plt

x = np.linspace(0,6,1000)
y = np.cos(2*np.pi*x)*np.exp(-x)+1.2

plt.axis([np.min(x),np.max(x),0,np.max(y)])     #坐标范围
plt.plot(x,y,label="$cos(2πx)e^{-x}+1.2$")      #画曲线，带图示
plt.fill_between(x,y1=y,y2=0,where=(x>=0.7)&(x<=4),   #填充积分区域
                 facecolor='blue',alpha=0.2)
plt.text(0.5*(0.7+4),0.4,r"$\int_{0.7}^4(cos(2πx)e^{-x}+1.2)\mathrm{d}x$",
         horizontalalignment='center',fontsize=14)          #增加说明文本
plt.legend()                                    #显示图示
plt.show()

