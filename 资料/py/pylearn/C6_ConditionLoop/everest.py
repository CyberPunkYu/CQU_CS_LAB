#everest.py
iCounter = 0                    #对折次数
fThickness = 0.0001             #纸厚，单位米
while True:
    if fThickness > 8844.43:    #超过珠峰高度就停止循环
        break
    else:
        fThickness *= 2         #对折一次厚度翻倍
        iCounter += 1           #对折次数加1

print("纸对折%d次后的厚度为%.2f米,超过了珠穆朗玛峰." % 
     (iCounter,fThickness))

import math
print(math.log2(8844.43/0.0001))

print(0.0001*(2**27))

