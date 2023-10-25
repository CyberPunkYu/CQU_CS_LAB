def myprint(title, name, gender, age, salary):
    print(title,":")
    print("\tname:\t",name)
    print("\tage:\t",age)
    print("\tsalary:\t",salary)

dora = ("Dora's Info", 'Dora Chen', 'female',26,3200)
myprint(*dora)

dora2 = dict(name="Dora Chen", age=26, gender='female',salary=3200)
myprint("Dora's Info", **dora2)