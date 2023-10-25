from api import sql

def insUserRegionWordAll():
    s1 = "insert into userRegionWordAll values "
    s = "select * from userRegionWord"
    data = sql.getData(s)
    for row in data:
        city = row[0]
        word = row[1].split(" @#$#@ ")[:50]
        num  = row[2].split(" @#$#@ ")[:50]
        for i in range(50):
            tmp = "('" + city + "'" + "," + "'" + word[i] + "'" + "," + "'" + str(num[i]) + "'),"
            s1 += tmp
    s1 = s1[:len(s1)-1]
    # print(s1)
    sql.exeSql(s1)
# insUserRegionWordAll()


def insListCommentWordAll():
    s1 = "insert into listCommentWordAll values "
    s = "select * from listCommentWord"
    data = sql.getData(s)
    for row in data:
        lname = row[1]
        word = row[2].split(" @#$#@ ")
        num  = row[3].split(" @#$#@ ")
        for i in range(len(word)):
            tmp = "('" + lname + "'" + "," + "'" + word[i] + "'" + "," + "'" + str(num[i]) + "'),"
            s1 += tmp
    s1 = s1[:len(s1)-1]
    # print(s1)
    sql.exeSql(s1)
# insListCommentWordAll()

def insSingerWordAll():
    s1 = "insert into singerWordAll values "
    s = "select * from singerWord"
    data = sql.getData(s)
    for row in data:
        sename = row[1]
        if(row[2] == ''):
            continue
        else:
            word = row[2].split(" @#$#@ ")
            num  = row[3].split(" @#$#@ ")
            for i in range(len(word)):
                tmp = "('" + sename + "'" + "," + "'" + word[i] + "'" + "," + "'" + str(num[i]) + "'),"
                s1 += tmp
    s1 = s1[:len(s1)-1]
    # print(s1)
    sql.exeSql(s1)
# insSingerWordAll()


def insSongCommentWordAll():
    s1 = "insert into songCommentWordAll values "
    s = "SELECT noUse.sname,songCommentWord.cword,songCommentWord.ccnt \
        FROM noUse LEFT JOIN songCommentWord \
        ON noUse.sname = songCommentWord.sname;"
    ans = set()
    data = sql.getData(s)
    for row in data:
        sname = row[0]
        if(sname in ans):
            continue
        else:
            ans.add(sname)
            word = row[1].split(" @#$#@ ")[::-1]
            num  = row[2].split(" @#$#@ ")[::-1]
            length = min(len(word), 100)
            for i in range(length):
                if(sname == 'I\'ll Do It (Sped Up Version)'):
                    sname = 'I\\\'ll Do It (Sped Up Version)'
                if(sname == 'Baby, Don\'t Cry (人鱼的眼泪)'):
                    sname = 'Baby, Don\\\'t Cry (人鱼的眼泪)'
                if(sname == '[Drill] Central Cee Type Drill Beat \'\'Somebody\'\''):
                    sname = '[Drill] Central Cee Type Drill Beat \\\'\\\'Somebody\\\'\\\''
                if(sname == '[Drill] Central Cee Type Drill Beat \'\'Lemonade\'\''):
                    sname = '[Drill] Central Cee Type Drill Beat \\\'\\\'Lemonade\\\'\\\''
                tmp = "('" + sname + "'" + "," + "'" + word[i] + "'" + "," + "'" + str(num[i]) + "'),"
                # print(tmp)
                s1 += tmp
    s1 = s1[:len(s1)-1]
    # print(s1)
    sql.exeSql(s1)
insSongCommentWordAll()



def insNoUse():
    s1 = "insert into noUse values "
    s = "select * from listSong"
    data = sql.getData(s)
    ans = set()
    for row in data:
        song = row[2].split(" @#$#@ ")
        if(len(song)):
            for i in range(len(song)):
                if(song[i] == 'I\'ll Do It (Sped Up Version)'):
                    song[i] = 'I\\\'ll Do It (Sped Up Version)'
                if(song[i] == 'Baby, Don\'t Cry (人鱼的眼泪)'):
                    song[i] = 'Baby, Don\\\'t Cry (人鱼的眼泪)'
                if(song[i] == '[Drill] Central Cee Type Drill Beat \'\'Somebody\'\''):
                    song[i] = '[Drill] Central Cee Type Drill Beat \\\'\\\'Somebody\\\'\\\''
                if(song[i] == '[Drill] Central Cee Type Drill Beat \'\'Lemonade\'\''):
                    song[i] = '[Drill] Central Cee Type Drill Beat \\\'\\\'Lemonade\\\'\\\''
                ans.add(song[i])
    for i in ans:
        tmp = "('" + i + "'),"
        s1 += tmp
    s1 = s1[:len(s1)-1]
    # print(s1)
    sql.exeSql(s1)
# insNoUse()