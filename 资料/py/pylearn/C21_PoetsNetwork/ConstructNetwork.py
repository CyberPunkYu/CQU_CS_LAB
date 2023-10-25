import sqlite3
from Utils import getPoetByName,Poet,Poem
from ProgressBar import printProgressBar

def loadPoemsPoets():
    fProgress = 0
    sPrefix = "诗/诗人筛选准备:"
    printProgressBar(fProgress, prefix=sPrefix)
    poems,poets = [],{}   #poets内的键值对形式 name:Poet对象

    dbCon = sqlite3.connect(dbFileName)
    dbCursor = dbCon.cursor()
    dbCursor.execute("SELECT id, title, author, content FROM poem")
    r = dbCursor.fetchall()

    for x in r:
        m = Poem(*x)   #x类型为元组，*x表示将元组展开，其元素逐一对应Poem构造函数参数
        t = poets.get(m.author,None) or getPoetByName(m.author,dbCon)
        if t:	#唐诗的诗人在poet表中存在
            poems.append(m)
            poets[m.author] = t
        fProgress += 0.5/len(r)
        printProgressBar(fProgress,prefix=sPrefix)

    dbCon.close()
    return poems,poets

def buildPoetsNetwork():
    references = [] #引用关系  (authorid, refid, poemid)
    poems,poets = loadPoemsPoets()

    fProgress = 0.3
    sPrefix = "引用关系发现:"
    printProgressBar(fProgress,prefix=sPrefix)

    for m in poems:
        authorId = poets[m.author].id
        for poet in poets.values():
            if m.title.find(poet.name) >= 0 or m.content.find(poet.name) >= 0:   
                references.append((authorId,poet.id,m.id))  #直接引用了本名
                continue

            for altName in poet.altNames:   #尝试别名
                if m.title.find(altName) >= 0 or m.content.find(altName) >= 0:
                    references.append((authorId,poet.id,m.id))
                    break
        fProgress += 0.45 /len(poems)
        printProgressBar(fProgress,prefix=sPrefix)
    
    printProgressBar(fProgress,prefix="引用关系保存:")
    dbCon = sqlite3.connect(dbFileName)
    dbCursor = dbCon.cursor()
    dbCursor.execute("DELETE FROM reference")
    dbCursor.executemany("INSERT INTO reference VALUES (?,?,?)", references)
    dbCon.commit()
    dbCon.close()
    printProgressBar(1.0,prefix="引用关系保存:")

dbFileName='data/data.db'
buildPoetsNetwork()
print("\n引用关系构建完成.")