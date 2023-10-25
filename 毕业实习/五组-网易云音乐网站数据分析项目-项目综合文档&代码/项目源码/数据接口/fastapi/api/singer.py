from fastapi import APIRouter, FastAPI
# 让数据以json的格式返回
from fastapi.responses import JSONResponse
import os, uuid
from . import sql
import sys
sys.path.append('/home/prj/fastapi/func')

from singerFunc import *
# 构建api路由
router_info = APIRouter(tags=["歌手分析"])

# 测试
# @router_info.get("/test")
# async def root():
#     return {"message": "success"}


# @router_info.get("/num/{singer}")
# async def root(singer: str):
#     return getSingerNum(singer)

# @router_info.get("/emo/{singer}")
# async def root(singer: str):
#     return getSingerEmo(singer)

# @router_info.get("/song/{singer}")
# async def root(singer: str):
#     return getSingerSong(singer)

# @router_info.get("/style/{singer}")
# async def root(singer: str):
#     return getSingerStyle(singer)

# @router_info.get("/Top/{singer}")
# async def root(singer: str):
#     return getSingerTop(singer)

# @router_info.get("/word/{singer}")
# async def root(singer: str):
#     return getSingerword(singer)

@router_info.get("/num")
async def root():
    s = "select * from singerAllNum"
    data = sql.getData(s)
    jsonData = []
    for row in data:
        tmp = {}
        tmp['sename'] = row[1]
        tmp['cnum']  = row[2]
        tmp['pnum']  = row[3]
        tmp['mnum']  = row[4]
        jsonData.append(tmp)
    return jsonData

@router_info.get("/song")
async def root():
    s = "select * from singerSong"
    data = sql.getData(s)
    jsonData = []
    for row in data:
        sename = row[1]
        song = row[2].split(" @#$#@ ")
        for i in range(len(song)):
            tmp = {}
            tmp['sename'] = sename
            tmp['song']  = song[i]
            jsonData.append(tmp)
    return jsonData


@router_info.get("/style")
async def root():
    s = "select * from singerStyle"
    data = sql.getData(s)
    jsonData = []
    for row in data:
        sename = row[1]
        word = row[2].split(" @#$#@ ")
        num  = row[3].split(" @#$#@ ")
        for i in range(len(word)):
            tmp = {}
            tmp['sename'] = sename
            tmp['word']  = word[i]
            tmp['num']   = num[i]
            jsonData.append(tmp)
    return jsonData

@router_info.get("/emo")
async def root():
    s = "select * from singerEmo"
    data = sql.getData(s)
    jsonData = []
    for row in data:
        sename = row[1]
        emo  = row[2].split(" @#$#@ ")
        num  = row[3].split(" @#$#@ ")
        for i in range(len(emo)):
            tmp = {}
            tmp['sename'] = sename
            tmp['emo']   = emo[i]
            tmp['num']   = num[i]
            jsonData.append(tmp)
    return jsonData


@router_info.get("/top")
async def root():
    s = "select * from singerTop10Song"
    data = sql.getData(s)
    jsonData = []
    for row in data:
        sename = row[1]
        song = row[2].split(" @#$#@ ")
        num  = row[3].split(" @#$#@ ")
        for i in range(len(song)):
            tmp = {}
            tmp['sename'] = sename
            tmp['song']  = song[i]
            tmp['num']   = num[i]
            jsonData.append(tmp)
    return jsonData