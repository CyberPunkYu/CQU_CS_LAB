def myprint(title, **contents):
    print(title,":")
    for k,v in contents.items():
        print("\t", k+":\t", v)
    print(type(contents))

myprint("Dora's Information", name="Dora Chen", age=26, salary=3200)