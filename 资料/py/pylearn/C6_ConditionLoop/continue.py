#continue.py
names = ['Peter Anderson', 'Frank Bush', 'Tom Henry', 'Jack Lee','Dorothy Henry']  #1
                                            #2
i = 0                                       #3
henrys = []                                 #4
while i < len(names):                       #5
    sName = names[i]                        #6
    i += 1                                  #7
    if not sName.endswith("Henry"):         #8
        continue                            #9
    print("Hi,", sName)                     #11
    henrys.append(sName)                    #12
                                            #13
print("We found following henry:", henrys)  #14