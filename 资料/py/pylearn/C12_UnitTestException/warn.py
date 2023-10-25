from warnings import warn

def divide(a,b):
    fResult = a / b
    if fResult < 0.0000001:
        warn("The result is very close to Zero!")
    return fResult

print(divide(0.1, 10000000000))
print("Something else.")