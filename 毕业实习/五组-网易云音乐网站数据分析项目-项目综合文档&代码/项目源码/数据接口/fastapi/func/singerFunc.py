import sys
sys.path.append('/home/prj/fastapi/api')
from sql import *


def getSingerNum(singer):
    s = "select cnum,pnum,mnum from singerAllNum where sename = \"" + singer + "\""
    data = getData(s)
    jsondata = []
    result = {}
    result['cnum'] = data[0][0]
    result['pnum'] = data[0][1]
    result['mnum'] = data[0][2]
    jsondata.append(result)
    return jsondata

def getSingerEmo(singer):
    s = "select emo,num from singerEmo where sename = \"" + singer + "\""
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

def getSingerSong(singer):
    s = "select songs from singerSong where sename = \"" + singer + "\""
    data = getData(s)
    jsondata = []
    result = {}
    result['songs'] = data[0][0].split(" @#$#@ ")
    jsondata.append(result)
    return jsondata

def getSingerStyle(singer):
    s = "select style,num from singerStyle where sename = \"" + singer + "\""
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

def getSingerTop(singer):
    s = "select hotsong,num from singerTop10Song where sename = \"" + singer + "\""
    data = getData(s)
    hotsong = data[0][0].split(" @#$#@ ")
    num = data[0][1].split(" @#$#@ ")
    jsondata = []
    for i in range(len(num)):
        result = {}
        result['hotsong'] = hotsong[i]
        result['num'] = num[i]
        jsondata.append(result)
    return jsondata

def getSingerWord(singer):
    s = "select word,cnt from singerWord where sename = \"" + singer + "\""
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