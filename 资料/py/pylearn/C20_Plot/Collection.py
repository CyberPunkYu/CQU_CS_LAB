import numpy as np
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt

patches = [
    Circle((0.1,0.1),.2),     #三个圆
    Circle((0.15,0.2),.15),
    Circle((0.3,0.4),.1) ]

patches += [
    Wedge((.2, .7), .1, 0, 360),   #0-360度的扇形 --> 实心整圆
    Wedge((.7, .8), .2, 0, 360, width=0.05), #宽度为0.05的圆环
    Wedge((.6, .3), .2, 0, 45),              #0-45度扇形
    Wedge((.8, .3), .2, 45, 90, width=0.1), #45-90度的扇形环,宽度 0.1
]

np.random.seed(20190522)    #用相同值初始化随机数种子，结果可重复
polygon = Polygon(np.random.rand(6, 2), True)   #六边形
patches.append(polygon)

colors = 100*np.random.rand(len(patches))   #为每个patch生成随机颜色值
pc = PatchCollection(patches, alpha=0.7)    #创建PatchCollection
pc.set_array(colors)                        #设置集合中每个Patch的颜色

fig, ax = plt.subplots()
ax.add_collection(pc)    #将PatchCollection加入子图Axes的collections列表
fig.colorbar(pc, ax=ax)  #为子图Axes添加颜色条
plt.show()