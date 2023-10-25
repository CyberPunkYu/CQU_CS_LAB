import struct 

fileName = "ergcurve.dat"
f = open(fileName,"rb")
rawData = f.read()   #bytes
f.close()

iSampleCount = len(rawData)//4
curveData = []
for i in range(iSampleCount):
    fValue, = struct.unpack("<f",rawData[i*4:i*4+4])
    curveData.append(fValue)

print(curveData)
import matplotlib.pyplot as plt
plt.plot(curveData)
plt.show()




