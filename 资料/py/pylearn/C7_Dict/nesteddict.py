jack = {'id':'10000', 'name':'Jack Ma',  'gender':'male',
        'age':47, 'title':'CEO'}
mary = {'id':'10001', 'name':'Mary Lee', 'gender':'female',
        'age':25, 'title':'Secretary'}
tom  = {'id':'10002', 'name':'Tom Henry','gender':'male',
        'age':28, 'title':'Engineer'}
dora = {'id':'10003', 'name':'Dora Chen','gender':'female',
        'age':32, 'title':'Sales'}

employees = {'10000':jack, '10001':mary, '10002':tom, '10003':dora}

sId = input("Please input the employee id:")
if sId not in employees:
    print("The ID does not exist.")
else:
    e = employees[sId]
    print("The employee's information is listed below:")
    print("ID:\t",e["id"])
    print("name:\t",e["name"])
    print("gender:\t",e["gender"])
    print("age:\t",e["age"])
    print("title:\t",e["title"])