import pymysql

def getData(sql):
    connect = pymysql.connect(
                            host='762j782l06.zicp.fun',
                            user='root',
                            password='12345678',
                            db='visualData',
                            port=50919,
                            charset='utf8')

    cur = connect.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    return data

def exeSql(sql):
    connect = pymysql.connect(
                            host='762j782l06.zicp.fun',
                            user='root',
                            password='12345678',
                            db='visualData',
                            port=50919,
                            charset='utf8')
    cur = connect.cursor()
    cur.execute(sql)
    connect.commit()
    cur.close()