import sqlite3

def parsePoemsIntoDatabase(txtFileName,dbFileName):
    dbCon = sqlite3.connect(dbFileName)		#创建数据库连接
    dbCursor = dbCon.cursor()				#创建一个游标-cursor
    dbCursor.executescript("""				
        DROP TABLE IF EXISTS poem;
        CREATE TABLE poem(id INT PRIMARY KEY ASC, title TEXT, author TEXT, content TEXT);
        """)  #通过SQL语句删除并重新创建poem表

    poems,idx = [],0  #[(0,'留别王维','孟浩然','寂寂...'),(1,'出塞','王昌龄','秦时..'),...]
    with open(txtFileName,"r",encoding="utf-8") as f:
        for line in f:
            txtSegments = line.split()
            poems.append((idx,txtSegments[1],txtSegments[2],txtSegments[-1]))
            idx+=1
    dbCursor.executemany("INSERT INTO poem VALUES (?,?,?,?)", poems) #向表格插入数据
    dbCon.commit()	#事务提交
    dbCon.close()	#关闭数据库连接

print("Start...")
parsePoemsIntoDatabase(txtFileName='data/qts_zht.txt',dbFileName='data/data.db')
print("End...")
