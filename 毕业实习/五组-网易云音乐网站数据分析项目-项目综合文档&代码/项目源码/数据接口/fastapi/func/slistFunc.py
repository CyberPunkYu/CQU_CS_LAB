import sys
sys.path.append('/home/prj/fastapi/api')
from sql import *


def getListAllNum(slist):
    s = "select cnum,pnum,bnum,mnum from singerAllNum where lname = \"" + slist + "\""
    data = getData(s)
    jsondata = []
    result = {}
    result['cnum'] = data[0][0]
    result['pnum'] = data[0][1]
    result['bnum'] = data[0][2]
    result['mnum'] = data[0][3]
    jsondata.append(result)
    return jsondata

def getCommentWord(slit):
    s = "select word,cnt from listCommentWord where lname = \"" + slist + "\""
    data = getData(s)
    word = data[0][0].split(" @#$#@ ")
    cnt = data[0][1].split(" @#$#@ ")
    jsondata = []
    for i in range(len(cnt)):
        result = {}
        result['word'] = word[i]
        result['cnt'] = cnt[i]
        jsondata.append(result)
    return jsondata

def getListEmo(slist):
    s = "select emo,num from listEmo where lname = \"" + slist + "\""
    data = getData(s)
    emo = data[0][0].split(" @#$#@ ")
    num = data[0][1].split(" @#$#@ ")
    jsondata = []
    for i in range(len(emo)):
        result = {}
        result['emo'] = emo[i]
        result['num'] = num[i]
        jsondata.append(result)
    return jsondata

def getListStyle(slist):
    s = "select style,num from listStyle where lname = \"" + singer + "\""
    data = getData(s)
    style = data[0][0].split(" ")
    num = data[0][1].split(" ")[1:]
    jsondata = []
    for i in range(len(num)):
        result = {}
        result['style'] = style[i]
        result['num'] = num[i]
        jsondata.append(result)
    return jsondata