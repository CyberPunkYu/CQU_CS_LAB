class Fibonacci:
    def __init__(self, max):
        self.a = 1
        self.b = 1
        self.idx = 0
        self.maxIdx = max

    def __iter__(self):
        return self

    def __next__(self):
        self.idx += 1
        if self.idx == 1:
            return 1
        elif self.idx == 2:
            return 1
        elif self.idx > self.maxIdx:
            raise StopIteration
        else:
            c = self.a + self.b
            self.a, self.b = self.b, c
            return c


for x in Fibonacci(10):
    print(x, end=",")

print("")
it = Fibonacci(10)
for x in range(10):
    print(next(it), end=",")

print("")
print(list(Fibonacci(10)))