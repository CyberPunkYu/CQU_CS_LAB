# 容器
import uvicorn, time
# FASTAPI模板
from fastapi import FastAPI
# 注册相应的api
from api import user, song, singer, slist
# 声明fastapi的实例
app = FastAPI(title="网易云音乐网站数据分析", version="2.4.0", description="dataease 数据源API接口")

# 注册api模块
app.include_router(user.router_info, prefix="/user")
app.include_router(singer.router_info, prefix="/singer")
app.include_router(song.router_info, prefix="/song")
app.include_router(slist.router_info, prefix="/slist")

# 配置容器启动相应的实例
if __name__ == '__main__':
    print("启动容器，时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    uvicorn.run(app='main:app',
                host='0.0.0.0',
                port=8087,
                reload=True)