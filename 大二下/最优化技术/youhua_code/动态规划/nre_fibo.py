import numpy as np
def nre_fibo(n):
    fi=np.zeros(n+1)
    fi[1]=1
    fi[2]=1
    for i in range(3,n+1):
        fi[i]=fi[i-1]+fi[i-2]
    return fi[n]

print(nre_fibo(7))
    
