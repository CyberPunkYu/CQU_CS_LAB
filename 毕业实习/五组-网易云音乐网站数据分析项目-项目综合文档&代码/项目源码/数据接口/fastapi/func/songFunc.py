import sys
sys.path.append('/home/prj/fastapi/api')
from sql import *


def getSongAge(song):
    s = "select age,emo,num from songAge where sname = \"" + song + "\""
    data = getData(s)
    age = data[0][0].split(" @#$#@ ")
    emo = data[0][1].split(" @#$#@ ")
    num = data[0][2].split(" @#$#@ ")
    jsondata = []
    for i in range(len(emo)):
        result = {}
        result['age'] = age[i]
        result['emo'] = emo[i]
        result['num'] = num[i]
        jsondata.append(result)
    return jsondata

def getCommentWord(song):
    s = "select cword,ccnt from songCommentWord where sname = \"" + song + "\""
    data = getData(s)
    cword = data[0][0].split(" @#$#@ ")
    ccnt  = data[0][1].split(" @#$#@ ")
    jsondata = []
    for i in range(len(ccnt)):
        result = {}
        result['ccnt']  = ccnt[i]
        result['cword'] = cword[i]
        jsondata.append(result)
    return jsondata

def getSongInfo(song):
    s = "select style,re from songInfo where sname = \"" + song + "\""
    data = getData(s)
    jsondata = []
    result = {}
    result['style'] = data[0][0]
    result['re'] = data[0][1]
    jsondata.append(result)
    return jsondata

def getSongRegion(song):
    s = "select cname,cnum from songRegion where sname = \"" + song + "\""
    data = getData(s)
    cname = data[0][0].split(" @#$#@ ")
    cnum  = data[0][1].split(" @#$#@ ")
    jsondata = []
    for i in range(len(cnum)):
        result = {}
        result['cnum']  = cnum[i]
        result['cname'] = cname[i]
        jsondata.append(result)
    return jsondata

def getSongSex(song):
    s = "select sex,num from songSex where sname = \"" + song + "\""
    data = getData(s)
    sex = data[0][0].split(" @#$#@ ")
    num  = data[0][1].split(" @#$#@ ")
    jsondata = []
    for i in range(len(num)):
        result = {}
        result['num']  = num[i]
        result['sex'] = sex[i]
        jsondata.append(result)
    return jsondata

def getWord(song):
    s = "select word,cnt from songWord where sname = \"" + song + "\""
    data = getData(s)
    word = data[0][0].split(" @#$#@ ")
    cnt  = data[0][1].split(" @#$#@ ")
    jsondata = []
    for i in range(len(cnt)):
        result = {}
        result['cnt']  = cnt[i]
        result['word'] = word[i]
        jsondata.append(result)
    return jsondata