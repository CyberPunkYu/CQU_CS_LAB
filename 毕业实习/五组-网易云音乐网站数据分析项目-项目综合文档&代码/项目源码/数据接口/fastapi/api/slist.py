from fastapi import APIRouter, FastAPI
# 让数据以json的格式返回
from fastapi.responses import JSONResponse
import os, uuid
from . import sql
import sys
sys.path.append('/home/prj/fastapi/func')

from slistFunc import *
# 构建api路由
router_info = APIRouter(tags=["歌单分析"])

# 测试
# @router_info.get("/test")
# async def root():
#     return {"message": "success"}


#***********************占位***********************
# @router_info.get("/allnum/{slist}")
# async def root(slist: str):
#     return getListAllNum(slist)

# @router_info.get("/commentword/{slist}")
# async def root(slist: str):
#     return getCommentWord(slist)

# @router_info.get("/emo/{slist}")
# async def root(slist: str):
#     return getListEmo(slist)

# @router_info.get("/style/{slist}")
# async def root(slist: str):
#     return getListStyle(slist)

@router_info.get("/commentWord")
async def root():
    s = "select * from listCommentWord"
    data = sql.getData(s)
    jsonData = []
    for row in data:
        lname = row[1]
        word = row[2].split(" @#$#@ ")
        num  = row[3].split(" @#$#@ ")
        for i in range(len(word)):
            tmp = {}
            tmp['lname'] = lname
            tmp['word']  = word[i]
            tmp['num']   = num[i]
            jsonData.append(tmp)
    return jsonData

@router_info.get("/listStyle")
async def root():
    s = "select * from listStyle"
    data = sql.getData(s)
    jsonData = []
    for row in data:
        lname = row[1]
        style = row[2].split(" @#$#@ ")
        num  = row[3].split(" @#$#@ ")
        for i in range(len(style)):
            tmp = {}
            tmp['lname'] = lname
            tmp['style']  = style[i]
            tmp['num']   = num[i]
            jsonData.append(tmp)
    return jsonData

@router_info.get("/listSong")
async def root():
    s = "select * from listSong"
    data = sql.getData(s)
    jsonData = []
    for row in data:
        lname = row[1]
        song = row[2].split(" @#$#@ ")
        for i in range(len(song)):
            tmp = {}
            tmp['lname'] = lname
            tmp['song']  = song[i]
            jsonData.append(tmp)
    return jsonData

@router_info.get("/listEmo")
async def root():
    s = "select * from listEmo"
    data = sql.getData(s)
    jsonData = []
    for row in data:
        lname = row[1]
        emo = row[2].split(" ")
        num  = row[3].split(" @#$#@ ")
        for i in range(len(emo)):
            tmp = {}
            tmp['lname'] = lname
            tmp['emo']  = emo[i]
            tmp['num']  = num[i]
            jsonData.append(tmp)
    return jsonData

@router_info.get("/listAllNum")
async def root():
    s = "select * from listAllNum"
    data = sql.getData(s)
    jsonData = []
    for row in data:
        lname = row[1]
        cnum  = row[2]
        pnum  = row[3]
        bnum  = row[4]
        mnum  = row[5]
        tmp = {}
        tmp['lname'] = lname
        tmp['cnum']  = cnum
        tmp['pnum']  = pnum
        tmp['bnum']  = bnum
        tmp['mnum']  = mnum
        jsonData.append(tmp)
    return jsonData

