def initPerson(person,id,name,age,gender,title):
    assert type(person)==dict
    person["id"] = id
    person["name"] = name
    person["gender"] = gender
    person["age"] = age
    person["title"] = title
    person["salary"] = []

dora = {}
initPerson(dora,"10001","Dora Chen",26,'female','Sales')
print("dict dora after function call:\n",dora)