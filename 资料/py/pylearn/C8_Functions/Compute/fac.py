#fac.py
def factorial(n):
    print("factorial(%d) is called." % (n))
    if n==1:
        return 1
    r = n*factorial(n-1)
    return r

if __name__ == "__main__":
    print("6!=",factorial(6))