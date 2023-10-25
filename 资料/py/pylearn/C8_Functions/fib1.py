def fibonacci(n):
    if n <= 2:
        return 1
    a,b = 1,1           #最近两项的值，a为前前项，b为前项
    for x in range(3,n+1):
        v = a + b       #新值 = 前两项之和
        a,b = b,v       #a = b, b = v
    return v

for n in range(1,121):  #121确保数值列表包括120
    print("month:",n,"rabbits:",fibonacci(n))


