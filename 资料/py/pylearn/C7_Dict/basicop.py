dorothy = dict(name='Dorothy', id='10003', age=26)
print(len(dorothy))
print(dorothy["id"])
dorothy['gender'] = 'female'
del dorothy["id"]
print("dict after del:", dorothy)
if "age" in dorothy:
    print("Key age exists in dict dorothy.")