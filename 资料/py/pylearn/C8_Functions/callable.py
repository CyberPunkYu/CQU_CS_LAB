from math import sqrt

def add(x,y):
    return x+y

tmp = 1
print("sqrt callable:",callable(sqrt))
print("add callable:",callable(add))
print("tmp callable:",callable(tmp))