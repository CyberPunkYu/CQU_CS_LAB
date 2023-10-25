#ergshow.py
import struct

fileName = "D:\\pylearn\\C11_FileIO\\ergcurve.dat"  #完整路径
f = open(fileName,"rb")
rawData = f.read()
f.close()

iSampleCount = len(rawData) // 4
curveData = []
for i in range(iSampleCount):
    fValue, = struct.unpack("<f",rawData[i*4:i*4+4])
    curveData.append(fValue)

print(curveData)
import matplotlib.pyplot as plt
plt.plot(curveData)
plt.show()

# f = open("ergcurve2.dat","wb")
# for x in curveData:
#     data = struct.pack("<f",x)
#     f.write(data)
# f.close()