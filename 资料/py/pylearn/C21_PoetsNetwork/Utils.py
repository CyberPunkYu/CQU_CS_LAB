#Utils.py
class Poem:
    def __init__(self,id,title,author,content):
        self.id, self.title,self.author,self.content = id,title,author,content 

    def print(self):
        print(self.title, "["+self.author+"]")
        print(self.content)
        print()

class Poet:
    def __init__(self,id,name,birthyear,deathyear):
        self.id,self.name,self.birthyear,self.deathyear = id,name,birthyear,deathyear
        self.altNames = []

    def print(self):
        print("诗人：{}, 生卒年:{}-{}, 别名:{}".format(self.name,self.birthyear,
        self.deathyear,self.altNames))


def getPoetNameById(id,dbCon):
    dbCursor = dbCon.cursor()
    dbCursor.execute('SELECT name FROM poet WHERE id = ?',(id,))
    r = dbCursor.fetchall()
    assert len(r) == 1
    return r[0][0]

def getAltNamesById(id,dbCon):
    altNames = []
    dbCursor = dbCon.cursor()
    dbCursor.execute("SELECT name FROM altname WHERE id = ?",(id,))
    r = dbCursor.fetchall()
    for (x,) in r:
        if len(x) > 1:     #别名至少要有两个字   单字别名如 刺，德
            altNames.append(x)
    return altNames

def getPoetByName(sName,dbCon):
    yearTangStart, yearTangEnd = 618, 907 #唐建立及灭亡年份
    dbCursor = dbCon.cursor()
    dbCursor.execute('SELECT id, name, birthyear, deathyear FROM poet WHERE name like ?',('%'+sName+'%',))
    candidates = dbCursor.fetchall()   #数据库中查询的候选人列表
    candidatesFiltered = []            #按生卒年筛选过的候选人列表
    for id, name, birthyear,deathyear in candidates:
        if birthyear and deathyear:
            if birthyear < yearTangEnd and deathyear > yearTangStart:
                t = Poet(id,sName,birthyear,deathyear)
                t.altNames = getAltNamesById(id,dbCon)
                return t   #生卒年明确且与唐朝有交集，直接返回
        elif birthyear or deathyear:
            year = birthyear if birthyear else deathyear
            if year > yearTangStart and year < yearTangEnd:
                candidatesFiltered.append((id,sName,birthyear,deathyear))
    
    if len(candidatesFiltered) == 0 or len(candidatesFiltered) > 1:
        return None
    
    t = Poet(*candidatesFiltered[0])
    t.altNames = getAltNamesById(t.id,dbCon)
    return t