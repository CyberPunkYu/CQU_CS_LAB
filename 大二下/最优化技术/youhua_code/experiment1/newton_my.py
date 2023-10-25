import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def func1(x1,x2):  #目标函数
    return 60-10*x1-4*x2+x1**2+x2**2-x1*x2
def func2(x1,x2):  #对x1的一阶偏导数
    return -10+2*x1-x2
def func3(x1,x2):  #对x2的一阶偏导数
    return -4+2*x2-x1
def func4(x1,x2):  #f''11
    return 2
def func5(x1,x2):  #f''12
    return -1
def func6(x1,x2):  #f''21
    return -1
def func7(x1,x2):  #f''22
    return 2
def matric_first_D(x1,x2):  #一阶导矩阵
    return np.array([[func2(x1,x2)],[func3(x1,x2)]]) #2*1

matric_second_D = np.array([[func4(0,0), func5(0,0)], [func6(0,0), func7(0,0)]])  #二阶导矩阵
matric_second_D_inv = np.linalg.inv(matric_second_D)   #二阶导矩阵的逆矩阵  2*2

print(matric_second_D)
print(matric_second_D_inv)
print(matric_first_D(0,0))

def NewtonMethod(x10,x20,ep):
    flag = 0  #记录迭代次数
    print('第',flag,'次迭代, x1',flag,'x2',flag,'为: [',x10,',',x20,']')
    matric_x = np.array([[x10],[x20]])       #xk矩阵,当前x的值
    while 1:
        flag = flag + 1
        firstD=matric_first_D(matric_x[0][0],matric_x[1][0])   #一阶导函数
        matric_x1=matric_x-np.dot(matric_second_D_inv,firstD)  #一阶导函数和二阶导函数的逆相乘得到xk+1矩阵
        # print(matric_x1)
        if ((abs(matric_x1[0][0]-matric_x[0][0]) <= ep) & (abs(matric_x1[1][0]-matric_x[1][0]) <= ep)): #满足条件返回
            break
        matric_x=matric_x1 #下一轮迭代
        print('第',flag,'次迭代, x1',flag,'x2',flag,'为: [',matric_x[0][0],',',matric_x[1][0],']') #打印迭代过程
    return func1(matric_x[0][0],matric_x[1][0])
    
print("the mimum value is :",NewtonMethod(0,0,0))  #我们设置ep为0，得到精确解


fig = plt.figure() # 创建一个图像窗口
ax = Axes3D(fig) # 在图像窗口添加3d坐标轴
x = np.linspace(-10,10,50)# 使用np.linspace定义 x:范围(-10,10);个数为50
y = np.linspace(-10,10,50)# 定义 y:范围
x,y = np.meshgrid(x,y)# 创建x-y平面网络
r = 60-10*x-4*y+x**2+y**2-x*y# 定义函数
plt.xlabel('x')
plt.ylabel('y')
# 将函数显示为3d  rstride 和 cstride 代表 row(行)和column(列)的跨度 get_cmap为色图分类 
ax.plot_surface(x,y,r,rstride = 1, cstride = 1, cmap='rainbow')
plt.show()