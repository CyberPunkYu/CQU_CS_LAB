names = ['jack','mary','tom','dorothy','peter']
namesAssigned = names
namesCopy = names.copy()
namesCopy[1] = "FORD"
print("id:",id(names),"names:",names)
print("id:",id(namesAssigned),"namesAssigned:",namesAssigned)
print("id:",id(namesCopy), "namesCopy:",namesCopy)