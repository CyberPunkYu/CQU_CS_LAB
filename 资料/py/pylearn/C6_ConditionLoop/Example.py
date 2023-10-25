a,b,c = 0,1,1
while True:
    print(c)
    c = a + b
    a,b = b,c
    if c > 30:
        break

