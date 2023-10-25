#luckynumber.py
sName = input("Please input your english name:")
sName = sName.strip().lower()                  #去除首尾空格，并转换成小写
luckyNumber = 0
for x in sName:                                #循环遍历姓名中的每一个字母
    v = ord(x)-ord('a')+1                      #计算字母x对应的值
    luckyNumber += v                           #将值加入幸运数
    print("value of",x,"=",v)                  #打印中间过程，便于读者理解程序

print("Your lucky number is:",luckyNumber)     #打印幸运数
    
    