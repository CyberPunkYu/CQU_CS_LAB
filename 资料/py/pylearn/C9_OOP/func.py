class Person:
    def __init__(self):
        self.sName = ""
        self.sId = ""
        print("Person::__init__().")

    def eat(self,weight):
        print("Person::eat():", weight, "grams of food.")

dora = Person()
print(hasattr(dora,"sName"))
setattr(dora,"sName","Dora CHEN")
print(getattr(dora,"sName",None))
print(callable(getattr(dora,"eat",None)))