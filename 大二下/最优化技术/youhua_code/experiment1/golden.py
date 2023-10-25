import matplotlib.pyplot as plt
import numpy as np
import math

def  calFunc(x):  #目标函数
  return 8*(math.exp(1-x))+7*math.log(x,10)

def searchinterval(x0,h): #进退法求解搜索范围，输入初始点和步长
    x1=x0
    f1=calFunc(x1)
    x2=x1+h
    f2=calFunc(x2)
    while f1>f2:  #如果f2<f1,前进运算
        x3=x2+h
        f3=calFunc(x3)
        if f3>f2: #f3>f2,达到高低高，直接返回结果
            return [x1,x3]
        else:     #f3<=f2,双倍步长，重新循环
            h=2*h
            x1=x2      
            x2=x3
            f1=calFunc(x1)
            f2=calFunc(x2)
    
    while f1<f2:  #如果f2>f1,后退运算
        x1,x2=x2,x1 #反向操作
        f1,f2=f2,f1
        h=-h        #步长反向
        x3=x2+h
        f3=calFunc(x3)
        if f3>f2:   #与上一个循环一致
            return [x1,x3]
        else:
            h=2*h
            x1=x2      
            x2=x3
            f1=calFunc(x1)
            f2=calFunc(x2)

searching_range=[a,b]=searchinterval(1,1) #a,b为搜索范围，其中初始点为1，步长为1
print('the searching range is',searching_range)

        

def golden(a,b,ep):  #黄金分割法，其中输入为搜索范围和迭代精度
    flag = 0
    print('第',flag,'次迭代: a',flag,' = ',a,', b',flag,' = ',b)  #打印迭代过程和次数
    while 1:
        flag=flag+1
        if b-a<=ep:      #如果搜索范围以及小于等于精度，直接返回
            m=(a+b)/2
            print('迭代停止,极值点为: ',m)  #打印极值点
            return a,b,m

        a1=a+0.382*(b-a) #黄金分割中间过程
        a2=a+0.618*(b-a)
        f1=calFunc(a1)
        f2=calFunc(a2)

        if f1>f2:       
            a=a1
        else:       
            b=a2
        print('第',flag,'次迭代: a',flag,' = ',a,', b',flag,' = ',b)  #打印迭代过程和次数

ep=0.23         #精度设置为0.23
[xmin,xmax,xmedian]=golden(a,b,ep)
print("搜索范围是:[{},{}],极值点为={}".format(xmin,xmax,xmedian))

# plt.figure(1)  #作图
# x=np.arange(1,10,0.1)
# result = [calFunc(i) for i in x]
# plt.plot(x,result)
# plt.show()

plt.figure(1)
x=np.linspace(1,10,10)
result = [calFunc(i) for i in x]
plt.plot(x,result)
plt.show()