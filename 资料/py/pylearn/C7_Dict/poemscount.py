statPoets = {}  #字典, 键值对示例 - 李白：897

with open('qts_zht.txt',"r",encoding="utf-8") as f:
    for line in f:
        txtSegments = line.split()   #按空格拆分字符串
        sPoetName = txtSegments[2]   #第2列（从0开始计）为作者姓名
        statPoets[sPoetName] = statPoets.get(sPoetName,0) +  1

statPoetsList = []
for k,v in statPoets.items():  #将字典转入列表[...['李白',897]...['李商隐',555]...]
    statPoetsList.append([k,v])

statPoetsList.sort(key=lambda x:x[1],reverse=True)  #按作品数量从高到低排序
print(statPoetsList[:10])  #切片，取前十个元素