#Pie.py
import matplotlib.pyplot as plt

#2018年第三季度全球智能手机市场主要品牌出货量
labels = 'Samsung', 'Huawei', 'iPhone', 'MI','OPPO','Others'
sizes = [72.2, 52.0, 46.9, 34.3,29.9,119.9]  #数据单位: million/百万台
explode = (0.02, 0.02, 0.1, 0.02,0.02,0.02)  #第三项爆炸突出0.1，即iPhone

fig, ax = plt.subplots()
ax.pie(sizes, explode=explode, labels=labels, autopct='%.1f%%',
        shadow=False, startangle=90, colors=['gray']*6)
ax.axis('equal')  #各轴比例相同以确保饼图为正圆
plt.show()