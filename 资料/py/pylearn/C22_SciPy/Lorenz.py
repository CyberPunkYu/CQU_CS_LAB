#Lorenz.py
import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def lorenz(p,t,s,r,b):
    x,y,z = p.tolist()          #无质量点的当前位置(x,y,z)
    print("x,y,z,t:",x,y,z,t)   #帮助理解odeint的执行过程
    return s*(y-x),x*(r-z)-y,x*y-b*z #返回dx/dt,dy/dt,dz/dt

t = np.arange(0,30,0.01)
track1 = integrate.odeint(lorenz,(0.0,1.00,0.0),t,args=(10.0,28.0,2.6))
track2 = integrate.odeint(lorenz,(0.0,1.01,0.0),t,args=(10.0,28.0,2.6))
print("type(track1):",type(track1),"track1.shape:",track1.shape)

fig = plt.figure(figsize=(12,6))
ax = fig.gca(projection='3d')   #获取当前子图，指定三维模式
ax.plot(track1[:,0],track1[:,1],track1[:,2],lw=1.0,color='r')				#在当前子图中绘制吸引子曲线
ax.plot(track2[:,0],track2[:,1],track2[:,2],lw=1.0,color='g')				#在当前子图中绘制吸引子曲线
ax.set_xlabel("X Axis")			#设置各轴标题
ax.set_ylabel("Y Axis")
ax.set_zlabel("Z Axis")
ax.set_title("Lorenz Attractor")#设置子图标题
plt.show()