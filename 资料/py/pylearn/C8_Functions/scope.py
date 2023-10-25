def func():
    x = 77
    print("x inside func:", x)
    print("y inside func:", y)

x = 1
y = 2
func()
print("x outside func:", x)
print("y outside func:", y)