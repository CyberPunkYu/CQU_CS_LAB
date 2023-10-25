def func():
    global x
    y[1] = 99
    x = 77
    print("x inside func:", x)
    print("y inside func:", y)

x = 1
y = [3,2,1]
func()
print("x outside func:", x)
print("y outside func:", y)
