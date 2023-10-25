import sqlite3,math
from Utils import getPoetNameById

def dataPrepare(num):
    r = []  #[('李白','杜甫',3),('孟浩然','杜甫',12),...]
    sSql = """
        SELECT authorid, refid, count(*) as cnt 
        FROM reference
        GROUP BY authorid, refid 
        ORDER BY cnt DESC 
        LIMIT ?;"""

    dbCon = sqlite3.connect(dbFileName)
    dbCursor = dbCon.cursor()
    dbCursor.execute(sSql,(num,))
    s = dbCursor.fetchall()

    for authorid, refid, cnt in s:
        sAuthorName = getPoetNameById(authorid,dbCon)
        sRefName = getPoetNameById(refid,dbCon)
        r.append((sAuthorName,sRefName,cnt))
    
    dbCon.close()
    return r


def saveToHtml(r):
    #1.读取HTML头部文本 --> sHtmlHead
    with open('html/html_head.txt', 'r', encoding = 'utf-8') as f:
        sHtmlHead = f.read()

    #2.节点/Node之间的连接 ---> sLinks
    sLinks = 'links: [\n'
    linkFormat = """{source: '%s', target: '%s',
    lineStyle:{normal:{width: %f}}},"""
    authors = set()
    for sAuthorName,sRefName,cnt in r:
        authors.add(sAuthorName)
        authors.add(sRefName)
        sLinks += linkFormat % (sAuthorName,sRefName,math.sqrt(cnt))
    sLinks += '],\n'

    #3. 节点/Node  --->  sNodes
    sNodes = 'data:[\n'
    data_item_format = "{name: '%s'},\n"
    for author in authors:
        sNodes += data_item_format % author
    sNodes += '],\n'

    #4. 读取HTML尾部文本 ---> sHtmlTail
    with open('html/html_tail.txt', 'r', encoding = 'utf-8') as f:
        sHtmlTail = f.read()

    #5. 合并存储至HTML网页 sHtmlHead + sNodes + sLinks + sHtmlTail
    sHtmlFile = 'html/tang_poets_network_%s.html' % (len(r))
    with open(sHtmlFile, 'w', encoding = 'utf-8') as f:
        f.write(sHtmlHead + sNodes + sLinks + sHtmlTail)

    #6. 保存文本文件, 列:诗人  被引用人  次数
    sTxtFile = 'html/tang_poets_network_%s.txt' % (len(r))
    with open(sTxtFile,'w', encoding = 'utf-8') as f:
        f.write("诗人\t被引用人\t次数\n")
        for sAuthorName,sRefName,cnt in r:
            f.write(sAuthorName+"\t"+sRefName+"\t"+str(cnt)+"\n")

dbFileName='data/data.db'
print("Start...")
saveToHtml(dataPrepare(50))     #导出关系网络前50行
saveToHtml(dataPrepare(100))    #导出关系网络前100行
saveToHtml(dataPrepare(200))    #导出关系网络前200行
saveToHtml(dataPrepare(500))    #导出关系网络前500行
print("Finished.")