import sqlite3
from Utils import getPoetByName,Poem

def getReferencePoems(authorId,refId,dbCon):
    poems = []
    dbCursor = dbCon.cursor()
    sSql = "SELECT id, title, author, content FROM poem "\
    "WHERE id IN ( SELECT poemid FROM reference WHERE authorid = ? and refid = ?)"
    dbCursor.execute(sSql,(authorId,refId))
    r = dbCursor.fetchall()
    for id,title,author,content in r:
        m = Poem(id,title,author,content)
        poems.append(m)
    return poems

dbFileName='data/data.db'
dbCon = sqlite3.connect(dbFileName)

while True:
    sName1 = input("请输入第一位诗人的姓名:(q退出)")
    if sName1 == "q":
        break
    poet1 = getPoetByName(sName1.strip(),dbCon)
    if poet1 == None:
        print("没有找到这位诗人.")
        break
    
    sName2 = input("请输入第二位诗人的姓名:(q退出)")
    if sName2 == "q":
        break
    poet2 = getPoetByName(sName2.strip(),dbCon)
    if poet2 == None:
        print("没有找到这位诗人.")
        break

    poet1.print()
    poet2.print()

    poems = getReferencePoems(poet1.id,poet2.id,dbCon)
    print("------{}提及{},共{}次:--------".format(poet1.name,poet2.name,len(poems)))
    for m in poems:
        m.print()

    poems = getReferencePoems(poet2.id,poet1.id,dbCon)
    print("------{}提及{},共{}次:--------".format(poet2.name,poet1.name,len(poems)))
    for m in poems:
        m.print()
    
dbCon.close()
