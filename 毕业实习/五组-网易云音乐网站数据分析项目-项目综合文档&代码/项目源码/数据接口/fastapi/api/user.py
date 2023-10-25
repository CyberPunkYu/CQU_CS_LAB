from fastapi import APIRouter, FastAPI
# 让数据以json的格式返回
from fastapi.responses import JSONResponse
import os, uuid
from . import sql
import sys
sys.path.append('/home/prj/fastapi/func')

from userFunc import *
# 构建api路由
router_info = APIRouter(tags=["用户分析"])


@router_info.get("/userAge")
async def root():
    s = "select * from userAge"
    data = sql.getData(s)
    jsonData = []
    for row in data:
        result = {}
        result['age'] = row[0]
        result['aemo'] = row[1]
        result['anum'] = row[2]
        jsonData.append(result)
    return jsonData

@router_info.get("/userNum")
async def root():
    s = "select * from userNum"
    data = sql.getData(s)
    jsonData = []
    for row in data:
        result = {}
        result['unum'] = row[0]
        result['lnum'] = row[1]
        result['snum'] = row[2]
        result['senum'] = row[3]
        result['pnum'] = row[4]
        jsonData.append(result)
    return jsonData

@router_info.get("/userRegion")
async def root():
    s = "select * from userRegion"
    data = sql.getData(s)
    jsonData = []
    for row in data:
        result = {}
        result['cname'] = row[0]
        result['cemo'] = row[1]
        jsonData.append(result)
    return jsonData

@router_info.get("/userSex")
async def root():
    s = "select * from userSex"
    data = sql.getData(s)
    jsonData = []
    for row in data:
        result = {}
        result['sex'] = row[0]
        result['semo'] = row[1]
        jsonData.append(result)
    return jsonData


@router_info.get("/userRegionWord")
async def root():
    s = "select * from userRegionWord"
    data = sql.getData(s)
    jsonData = []
    for row in data:
        city = row[0]
        word = row[1].split(" @#$#@ ")
        num  = row[2].split(" @#$#@ ")
        for i in range(50):
            tmp = {}
            tmp['cname'] = city
            tmp['word']  = word[i]
            tmp['num']   = num[i]
            jsonData.append(tmp)
    return jsonData


@router_info.get("/userTop10City")
async def root():
    s = "select * from userTop10City"
    data = sql.getData(s)
    jsonData = []
    for row in data:
        result = {}
        result['cname'] = row[0]
        result['cemo'] = row[1]
        result['cnum'] = row[2]
        jsonData.append(result)
    return jsonData

# @router_info.get("/{city}")
# async def root(city: str):
#     return getRegionWord(city)
