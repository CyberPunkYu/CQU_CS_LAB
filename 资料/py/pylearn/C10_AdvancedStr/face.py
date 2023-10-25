#face.py
r = list(range(0x1f601,0x1f64f+1)) + list(range(0x2702,0x27b0+1)) \
    + list(range(0x1f680,0x1f6c0+1)) + list(range(0x1F681,0x1F6C5+1)) \
    + list(range(0x1F30D,0x1F567+1))

with open("face.txt","w",encoding="utf-8") as f:
    for idx,x in enumerate(r):
        if idx%50==0:						#每50个字符换一次行
            f.write("\n")
        f.write("{num:c}".format(num=x))