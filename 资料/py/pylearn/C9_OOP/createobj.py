from enum import Enum
class Gender(Enum):
    male = 0
    female = 1

class Person:
    "user defined class: Person"
    def __init__(self,idNo="N/A",name="N/A"):
        self.sName = name
        self.gender = Gender.male
        self.sId = idNo
        self.iWeight = 0

    def speak(self):
        print("Person::speak()")
        print("I am",self.sName,",","Nice to meet you here.")

    def eat(self,weight):
        self.iWeight += weight
        print("I just eat",weight,"gram's food.")

    def description(self):
        s = "ID:%s\tName:%s\n" % (self.sId,self.sName)
        t = "Gender:%s\tBody Weight:%d" % (
            'male' if self.gender == Gender.male else 'female',
            self.iWeight)
        return s + t

dora = Person("36040200001","Dora CHEN")
peter = Person("36040200002","Peter Lee")
dora.gender = Gender.female
dora.iWeight = 100000
dora.iHeight = 172
dora.eat(320)     #与Person.eat(dora,320)等价
print(dora.description())


jack = Person('0001','Jack Ma')
dora = Person('0002','Dora CHEN')
employees = [jack,dora]
for x in employees:
    x.speak()





