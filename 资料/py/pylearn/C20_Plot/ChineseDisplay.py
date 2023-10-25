from matplotlib import pyplot as plt
plt.rcParams["font.family"] = "SimHei"
plt.plot([1,2,1],label="中文演示")
plt.xlabel("字体变大",fontsize=15)
plt.legend()
plt.show()