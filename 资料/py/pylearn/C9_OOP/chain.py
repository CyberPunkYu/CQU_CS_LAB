class A:
    def __init__(self):
        print("A init.")

class B(A):
    def __init__(self):
        print("B init.")

class C(B):
    def __init__(self):
        print("C init.")

class D(C):
    def __init__(self):
        super(C,self).__init__()
        print("D init.")

d = D()