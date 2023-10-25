#fac.py
def factorial(n):
    if n==1:
        return 1
    r = n*factorial(n-1)
    return r

print(__name__)

if __name__ == "__main__":
    print("6!=",factorial(6))