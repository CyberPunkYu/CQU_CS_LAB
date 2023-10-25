def foo(x):
    "Function Foo."
    return x*x

print(type(foo),foo)
print(foo.__doc__)
print("foo.dir():",foo.__dir__())
func = foo
print(func(2))

class Dummy:
    "Class Dummy."
    def say(self):
        print("Dummy.")

print(type(Dummy), Dummy)
print(Dummy.__doc__)
Dummy2 = Dummy
d = Dummy2()
d.say()