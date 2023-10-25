a = 1
print("id:",id(a))
a = 2
print("id:",id(a))
b = a
print("id of a:", id(a), "id of b:",id(b))
a += 1
print("id:",id(a))