from enum import Enum

class Gender(Enum):
    male = 0
    female = 1

class Person:
    "user defined class: Person."
    def __init__(self,idNo="N/A",name="N/A"):
        self.sName = name
        self.gender = Gender.male
        self.sId = idNo
        self.iWeight = 0

    def speak(self):
        print("Person::speak():")
        print("I am", self.sName + ",", "Nice to meet you here.")

    def eat(self, weight):
        self.iWeight += weight
        print("I just eat", weight, "gram's food.")


    def description(self):
        assert self.gender in (Gender.female,Gender.male)
        s = "ID: %s\tName: %s \n" % (self.sId,self.sName)
        t = "Gender: %s\tBody Weight: %d" % (
            'Male' if self.gender == Gender.male else 'Female', 
            self.iWeight)
        return s + t
