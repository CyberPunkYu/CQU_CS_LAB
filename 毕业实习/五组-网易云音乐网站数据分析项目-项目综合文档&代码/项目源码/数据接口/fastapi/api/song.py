from fastapi import APIRouter, FastAPI
# 让数据以json的格式返回
from fastapi.responses import JSONResponse
import os, uuid
from . import sql
import sys
sys.path.append('/home/prj/fastapi/func')

from songFunc import *

# 构建api路由
router_info = APIRouter(tags=["歌曲分析"])

# 测试
# @router_info.get("/test")
# async def root():
#     return {"message": "success"}

##***********************占位***********************
# @router_info.get("/age/{song}")
# async def root(song: str):
#     return getSongAge(song)

# @router_info.get("/commentword/{song}")
# async def root(song: str):
#     return getCommentWord(song)

# @router_info.get("/info/{song}")
# async def root(song: str):
#     return getSongInfo(song)

# @router_info.get("/region/{song}")
# async def root(song: str):
#     return getSongRegion(song)

# @router_info.get("/sex/{song}")
# async def root(song: str):
#     return getSongSex(song)

# @router_info.get("/word/{song}")
# async def root(song: str):
#     return getSongWord(song)


@router_info.get("/belong")
async def root():
    s = "select * from listSong"
    data = sql.getData(s)
    jsonData = []
    for row in data:
        lname = row[1]
        song  = row[2].split(" @#$#@ ")
        for i in range(len(song)):
            tmp = {}
            tmp['lname'] = lname
            tmp['song']  = song[i]
            jsonData.append(tmp)
    return jsonData

@router_info.get("/recommand")
async def root():
    s = "select * from songInfo"
    data = sql.getData(s)
    jsonData = []
    for row in data:
        lname = row[1]
        song  = row[3].split(" @#$#@ ")
        for i in range(len(song)):
            tmp = {}
            tmp['lname'] = lname
            tmp['song']  = song[i]
            jsonData.append(tmp)
    return jsonData