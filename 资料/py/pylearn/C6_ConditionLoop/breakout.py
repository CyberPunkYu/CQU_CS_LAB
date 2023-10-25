names = ['Peter Anderson', 'Frank Bush', 'Tom Henry','Jack Lee', 'Dorothy Henry']

sName = "NOTFOUND"
for x in names:
    if x.endswith("Henry"):
        sName = x
        break
    print(x, "not ends with 'Henry'.")

print("I found a Henry:", sName)