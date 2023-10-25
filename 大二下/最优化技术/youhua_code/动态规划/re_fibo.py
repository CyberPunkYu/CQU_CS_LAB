
def re_fibo(n):
    if n==1:
        return 1
    if n==2:
        return 1
    return re_fibo(n-1)+re_fibo(n-2)


print(re_fibo(7))