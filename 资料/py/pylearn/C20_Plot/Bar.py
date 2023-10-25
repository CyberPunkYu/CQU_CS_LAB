import matplotlib.pyplot as plt

avgMen = (20, 35, 30, 35, 27)     #各组男性平均得分
stdMen = (2, 3, 4, 1, 2)          #各组男性分数的标准差
avgWomen = (25, 32, 34, 20, 25)   #各组女性平均得分
stdWomen = (3, 5, 2, 3, 3)        #各组女性分数的标准差

fig,ax = plt.subplots()
ax.set_ylabel('Scores')
ax.set_title('Scores by group and gender')
p1 = ax.bar((0,1,2,3,4), avgMen, 0.35, yerr=stdMen)
p2 = ax.bar((0,1,2,3,4), avgWomen, 0.35, bottom=avgMen, yerr=stdWomen)
print(p1)
ax.legend((p1[0], p2[0]), ('Men', 'Women')) #显式地定义图示
plt.show()