numbers = [x for x in range(10)]
numbersCopy = numbers[:]
print("id:", id(numbers), numbers)
print("id:", id(numbersCopy), numbersCopy)

numbersReversed = numbers[::-1]
print("numbersReversed:",numbersReversed)

numbers[3:5] = 77,88
print("numbers:",numbers)