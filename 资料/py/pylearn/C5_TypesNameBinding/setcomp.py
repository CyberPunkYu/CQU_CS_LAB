#setcomp.py
s1 = {1,2,3,4}
s2 = {3,4,5,6}
print("s1 & s2:", s1 & s2)  #交集
print("s1.intersection(s2):",s1.intersection(s2))

print("s1 | s2:", s1 | s2)  #并集
print("s1.union(s2):",s1.union(s2))

print("s1 - s2:", s1 - s2)  #差集
print("s1.difference(s2):",s1.difference(s2))

print("s1 ^ s2:", s1 ^ s2)  #补集
print("s1.symmetric_difference(s2):",s1.symmetric_difference(s2))