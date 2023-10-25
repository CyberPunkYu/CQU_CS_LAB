def greeting(n,gender='male'):
    n = n.title()
    s = "Mr " if gender=='male' else 'Miss '
    n=s+n
    print("Hi,",n)
    return

sName = "john henry"
greeting(sName)
print("sName after function call:",sName)
