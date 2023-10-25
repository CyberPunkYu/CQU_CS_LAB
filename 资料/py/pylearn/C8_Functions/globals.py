def func():
    x = 77
    print("local x:",x)
    print("global x:",globals()["x"])
    
x = 1
func()