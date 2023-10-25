def hanoi(n, a, b, c):
    if n == 1:
        yield (a,c)
    else:
        for x in hanoi(n - 1, a, c, b):
            yield x
        yield (a,c)
        for x in hanoi(n - 1, b, a, c):
            yield x


if __name__ == '__main__':
    genHanoi = hanoi(5, 0, 1, 2)
    while True:
        try:
            a = next(genHanoi)
        except (StopIteration,Exception) as e:
            break
        else:
            print(a)





