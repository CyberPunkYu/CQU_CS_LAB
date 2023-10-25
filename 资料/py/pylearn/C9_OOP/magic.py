class Person:
    def __init__(self,name="N/A"):
        self.sName = name
        print("Person::__init__")

    def __del__(self):
        print("Person::__del__")

d = Person("Dora")
c = d
d = None
print("--------------------------")
c = 2
print("**************************")