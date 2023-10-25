import sys

sContents = sys.stdin.read()
words = sContents.split()

wordsStat = {}
for x in words:
    wordsStat[x] = wordsStat.get(x,0) + 1

sOutput = ""
for k,v in wordsStat.items():
    sOutput = sOutput + k + ":" + str(v) + "\t"

print(sOutput)



