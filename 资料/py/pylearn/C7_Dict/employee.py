jack = ['10000', 'Jack Ma',   'male',   47, 'CEO']
mary = ['10001', 'Mary Lee',  'female', 25, 'Secretary']
tom  = ['10002', 'Tom Henry', 'male',   28, 'Engineer']
dora = ['10003', 'Dora Chen', 'female', 32, 'Sales']
employees = [jack,mary,tom,dora]

for e in employees:
    if e[0] == '10003':
        print("The designated employee have been found:", e)
        break
        