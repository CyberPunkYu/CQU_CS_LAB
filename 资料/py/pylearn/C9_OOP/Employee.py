
from Person import Person, Gender

class Employee(Person):
    def __init__(self,emplNo,idNo,name):
        super(Employee,self).__init__(idNo,name) #Person.__init__(self,idNo,name)更佳
        self.sEmployeeNo = emplNo
        self.sJobTitle = ""
        self.sDepartment = ""
        self.iWeekSalary = 0

    def work(self):
        print("I am a", self.sJobTitle + ","
              "I am working with my partners in department:",
              self.sDepartment)

    def speak(self):
        print("Employee::speak():")
        super().speak()             #等价于Person.speak(self)
        print("I am happy to work for you.")

    def description(self):
        assert self.gender in (Gender.female,Gender.male)
        s = "ID: %s\tEmployee No:%s\tName: %s \n" % \
            (self.sId,self.sEmployeeNo,self.sName)
        t = "Gender: %s\tJob Title: %s\tDepartment: %s\n" % (
            'Male' if self.gender == Gender.male else 'Female',
            self.sJobTitle, self.sDepartment)
        return s + t


dora = Employee("10001","36040200001","Dora CHEN")
dora.gender = Gender.female
dora.sDepartment = "Marketing"
dora.sJobTitle = "Sales"
dora.iWeekSalary = 2300

dora.work()
print()
dora.speak()
print()
dora.eat(220)
print()
print(dora.description())


# peter = Person("36040200002", "Peter Lee")
# peter.gender = Gender.male
# peter.iWeight = 120000
# peter.eat(320)
# print(peter.description())
#
# print(peter.sEmployeeNo)
