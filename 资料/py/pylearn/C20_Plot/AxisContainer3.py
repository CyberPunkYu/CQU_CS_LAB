from matplotlib.ticker import MultipleLocator,FuncFormatter
from matplotlib import pyplot as plt
import numpy as np

def pi_formater(x,idx): #x为刻度值，idx为刻度序号
    "将刻度值x转换成对应的刻度文本"
    print("inside pi_formater, x=",x,"idx:",idx)
    return r"$%.1f\pi$" % (x / np.pi)

x = np.linspace(0,4*np.pi,500)
fig,ax = plt.subplots(figsize=(10,5))
ax.plot(x,np.sin(x),label="sin(x)")
ax.plot(x,np.cos(x),label="cos(x)")

ax.xaxis.set_major_locator(MultipleLocator(np.pi/2))   #设主刻度为0.5π
ax.xaxis.set_minor_locator(MultipleLocator(np.pi/10))  #设副刻度为0.1π
ax.xaxis.set_major_formatter(FuncFormatter(pi_formater)) #设置新的刻度文件生成对象
plt.show()