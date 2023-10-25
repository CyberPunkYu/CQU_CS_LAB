
def hanoi(n, a, b, c):
    if n == 1:
        movements.append(a + " --> " + c)
    else:
        hanoi(n - 1, a, c, b)
        movements.append(a + " --> " + c)
        hanoi(n - 1, b, a, c)

movements = []
hanoi(16, 'A', 'B', 'C')
print("Steps count:",len(movements))
print("The first 3 steps are:", movements[:3])