import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def lorenz(x, y, z, s=10, r=28, b=2.667):
    dt = 0.01							#t上的步长
    xOffset = s*(y - x)*dt
    yOffset = (x*(r-z) - y)*dt
    zOffset = (x*y - b*z)*dt
    return xOffset,yOffset,zOffset

stepCnt = 10000							#积分总步数
xs = [0 for i in range(stepCnt+1)]		#包括10001个元素的一维数组
ys = xs[:]                              #切片复制
zs = xs[:]
xs[0], ys[0], zs[0] = (0., 1., 1.05)	#初始化出发点坐标

for i in range(stepCnt):				#对时间积分
    xOffset,yOffset,zOffset = lorenz(xs[i], ys[i], zs[i])
    xs[i + 1] = xs[i] + xOffset
    ys[i + 1] = ys[i] + yOffset
    zs[i + 1] = zs[i] + zOffset

fig = plt.figure(figsize=(7,4))
ax = fig.gca(projection='3d')			#获取当前子图，指定三维模式

ax.plot(xs, ys, zs, lw=0.5)				#在当前子图中绘制吸引子曲线
ax.set_xlabel("X Axis")					#设置各轴标题
ax.set_ylabel("Y Axis")
ax.set_zlabel("Z Axis")
ax.set_title("Lorenz Attractor")		#设置子图标题

plt.show()