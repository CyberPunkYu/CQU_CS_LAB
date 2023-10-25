#greeting.py
def greeting(name,gender):
    name = name.title()
    s = "Mr" if gender=='male' else 'Miss'
    print("Hi,",s,name)

greeting("henry",'male')