def fibonacci(n):
    if n <= 2:
        return 1
    a,b = 1,1           #最近两项的值，a为前前项，b为前项
    for x in range(3,n+1):
        v = a + b       #新值 = 前两项之和
        a,b = b,v       #a = b, b = v
    return v

x = list(range(1,31))           #1..30的数值列表
n2,n3,fn = [],[],[]             #依次为n的平方，n的立方，n值斐波那契
for v in x:                     #依次计算机各函数值
    n2.append(v*v)
    n3.append(v*v*v)
    fn.append(fibonacci(v))

print("n^2=",n2)
print("n^3=",n3)
print("fib(n)=",fn)

from matplotlib import pyplot as plt     #绘图部分
plt.plot(x,n2,color='black',label="$y=n^2$")
plt.plot(x,n3,linestyle="-.",color='black',label="$y=n^3$")
plt.plot(x,fn,linestyle="--",color='black',label="$y=fibonacci(n)$")
plt.legend()
plt.show()


