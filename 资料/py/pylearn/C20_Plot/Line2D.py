from matplotlib import pyplot as plt
import numpy as np

x = np.linspace(-5,5,200)
lines1 = plt.plot(x,np.cos(6*x)*np.exp(-x),label="$cos(6x)e^{-x}$")    #返回Line2D列表
print("type(lines1):",type(lines1))   #lines是列表
print("len(lines1):",len(lines1))
line = lines1[0]
print("type(line):",type(line))     #line是Line2D类型
line.set_alpha(0.5)                 #设置透明度
lines2 = plt.plot(x,-5*x*x+50,label="$-5x^2+50$")    #再画一条线
plt.setp(lines1+lines2,color="black",linewidth=4.0) #批量设置属性

plt.legend()
plt.show()
