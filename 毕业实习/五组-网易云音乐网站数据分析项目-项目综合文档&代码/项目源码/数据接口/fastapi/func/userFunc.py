import sys
sys.path.append('/home/prj/fastapi/api')
from sql import *


def getRegionWord(region):
    s = "select word,cnt from userRegionWord where cname = \"" + region + "\""
    data = getData(s)
    word = data[0][0].split(" ")
    cnt  = data[0][1].split(" ")
    jsondata = []
    for i in range(len(word)):
        result = {}
        result['word'] = word[i]
        result['cnt']  = cnt[i]
        jsondata.append(result)
    return jsondata
