#seq1.py
x,y = 'x','y'
x,y = y,x				  #两个变量的值交换
print(x,y)

numbers = 1,2,3			  #1,2,3被自动打包成元组(1,2,3)，然后赋值
print(type(numbers),numbers)
a,b,c = numbers			  #元组序列解包
print(a,b,c)

d,e,f = [4,5,6]			  #列表序列解包
print(d,e,f)

g,h,i = '789'			  #字符串序列解包
print(g,h,i)

j,k,l = b'\x10\x20\x30'	  #16进制的10,20,30分别对应十进制16,32,48
print(j,k,l)