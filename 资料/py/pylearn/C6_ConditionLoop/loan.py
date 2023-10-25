#loan.py
fBalance = 10000                              #贷款初始余额
fRate = 0.0005                                #日利万分之五
balances = []                                 #贷款余额列表
for i in range(365*30):
    fBalance = fBalance + fBalance*fRate      #贷款余额 = 本金 + 本金*利率
    balances.append(fBalance)                 #把贷款余额存入列表绘图用
print("30年后连本带利欠款总额: %.2f" % fBalance)

from matplotlib import pyplot as plt          #贷款余额 vs 天数增长曲线
plt.plot(list(range(365*30)),balances)
plt.title("Loan balance grow by days")
plt.show()





