#file1.py
f = open('datafile.txt','w')
f.write("This is a file which is writable in text mode.\n")
f.write("'w' means open file in write mode.\n")
f.close()

f = open("datafile.txt","r")
sLine1 = f.readline()
sLine2 = f.readline()
print(sLine1,sLine2)
f.close()