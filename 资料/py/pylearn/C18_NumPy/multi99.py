import numpy as np

def multi(i,j):
    return (i+1)*(j+1)

print(np.fromfunction(multi,(9,9)).astype(int))