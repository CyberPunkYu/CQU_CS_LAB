def myprint(title, *contents):
    print(title,":")
    for x in contents:
        print("\t",x)

myprint("Read-only data types", "int", "float", 
        "str", "tuple", "bytes", "...")