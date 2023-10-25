a = [1,2,3,[3,2,1]]
b = a.copy()
print("id(a):",id(a),"id(b):",id(b))
print("id(a[3]):",id(a[3]),"id(b[3]):",id(b[3]))
b[3][2] = 99
print(a,b)