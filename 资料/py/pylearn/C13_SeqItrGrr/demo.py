g1 = (x**2 for x in range(1,10,2))
print(g1,type(g1))

for x in g1:
    print(x,end=",")
