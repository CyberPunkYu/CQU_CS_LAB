names = ['Peter Anderson', 'Frank Bush', 'Tom Henry','Jack Lee', 'Dorothy Henry']
for x in names:
    if x.endswith("Bach"):
        print("I found a Bach:",x)
        break
    print(x, "not ends with 'Bach'.")
else:
    print("No Bach been found.")