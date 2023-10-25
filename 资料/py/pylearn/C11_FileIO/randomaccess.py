import io
f = open('randomaccess.txt',"w+")
sText = "".join((str(x) for x in range(30)))
f.write("汉" + sText)
f.seek(6)
f.write("OFFSET_6_")
print("Current file position after seek and write:", f.tell())
f.close()

f = open('randomaccess.txt',"r")
print("Content:")
print(f.read())
f.close()