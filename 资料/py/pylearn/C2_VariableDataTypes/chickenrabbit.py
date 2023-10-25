#chickenrabbit.py
iHeads = 35             #变量 - 头的数量
iFeet = 94              #变量 - 脚的数量
a = iFeet - 2*iHeads    #假设全部是鸡，余下的脚的数量
iRabbits = a / 2        #免的数量等于余下的脚数/2
iChicken = iHeads - iRabbits    #鸡的数量等于 头的数量 - 兔的数量
print("Number of chicken = %d," % iChicken, "Number of rabbits = %d" %
iRabbits) #输出
print(iFeet == iChicken*2+iRabbits*4) #验证脚数 = 鸡数*2 + 兔数*4
