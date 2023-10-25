class Person:
    def __init__(self):
        self.sName = ""
        self.sId = ""
        print("Person::__init__().")

    def eat(self,weight):
        print("Person::eat():", weight, "grams of food.")

class TaxPayer:
    def __init__(self):
        self.childrenCount = 0
        print("TaxPayer::__init__().")

    def compIncomeTax(self):
        print("TaxPayer::compIncomeTax().")
        return 0

class Employee(Person,TaxPayer):
    def __init__(self):
        super().__init__()
        TaxPayer.__init__(self)
        self.sEmployeeNo = ""
        self.iWeekSalary = 0
        print("Employee::__init__().")

    def work(self):
        print("Employee::work().")

dora = Employee()
dora.eat(330)
dora.work()
dora.compIncomeTax()