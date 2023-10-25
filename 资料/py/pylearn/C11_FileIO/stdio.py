import sys

f = open('input.txt','w')
f.write("Alex\n")
f.write("27\n")
f.close()

fIn = open('input.txt',"r")
sys.stdin = fIn
fOut = open('output.txt',"w")
sys.stdout = fOut
fError = open('error.txt','w')
sys.stderr = fError

sName = input("What's your name?")
iAge = int(input("How old are you?"))
print("Hi,", sName.title(), "You are {} year's old.".format(iAge))

fIn.close()
fOut.close()

raise Exception("ERROR INFO")
fError.close()