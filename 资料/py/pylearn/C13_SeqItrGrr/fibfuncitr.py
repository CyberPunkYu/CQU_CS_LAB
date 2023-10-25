def FibonacciGenerator(n):
    assert n > 2  # 为代码简单，作者要求n>2
    yield 1
    yield 1
    a = b = 1
    for i in range(3, n + 1):
        c = a + b
        a, b = b, c
        yield c


print(list(FibonacciGenerator(10)))

for x in FibonacciGenerator(10):
    print(x, end=",")

print("")  # 换行
g = FibonacciGenerator(10)
for i in range(10):
    print(next(g), end=":")

print("")
print(FibonacciGenerator)
print(g)