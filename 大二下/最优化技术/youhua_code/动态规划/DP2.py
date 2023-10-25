import numpy as np
a=[8,3,1,2,4,1,7]
#求一组不相邻数的最大和
#opt（i）:到第i个数时的求取的最大和
#optpaht(i):到第i个数时求最大和的数字组成
#
#
def optv(a):
    opt=np.zeros(len(a))
    optpath=[[] for i in range(len(a))]
    opt[0]=a[0]
    optpath[0]=str(a[0])
    opt[1]=max(a[0],a[1])
    optpath[1]=str(int(opt[1]))
    
    for k in range(2,len(a)):
        A=a[k]+opt[k-2]
        B=opt[k-1]
        opt[k]=max(A,B)
        if opt[k]==A:
            optpath[k]=str(a[k])
            optpath[k]=optpath[k]+optpath[k-2]
        else:
             optpath[k]=optpath[k-2]

    return opt[len(a)-1],optpath[len(a)-1]

print(optv(a))