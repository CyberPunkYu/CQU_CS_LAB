# 爬取相关数据

import json
import time
from urllib import request
from bs4 import BeautifulSoup

# 伪装请求头
headers = {
    'Host': 'music.163.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}


def get_comments(page):
    """
        获取评论信息
    """
    url = 'https://music.163.com/api/v1/resource/comments/R_SO_4_2004684052?limit=20&offset=' + str(page)   # 页面url
    req = request.Request(url, headers=headers)  #使用request封装url和头部信息
    response = request.urlopen(req)     # 请求页面

    # 将返回页面数据转为json格式
    content_json = json.loads(response.read().decode("utf-8"))

    with open('./test.json', 'w', encoding='utf-8') as file:
        json.dump(content_json, file)

    # 获取评论数据
    items = content_json['comments']
    for item in items:

        # 用户名
        user_name = item['user']['nickname'].replace(',', '，')
        print(user_name, end=" ")

        # 用户ID
        user_id = str(item['user']['userId'])
        print(user_id, end=" ")

        # 获取用户信息
        user_message = get_user(user_id)

        # 用户年龄
        user_age = str(user_message['age'])
        print(user_age, end=" ")

        # 用户性别
        user_gender = str(user_message['gender'])
        print(user_gender, end=" ")

        # 用户所在地区
        user_city = str(user_message['city'])
        print(user_city, end=" ")

        # # 个人介绍
        # user_introduce = user_message['sign'].strip().replace('\n', '').replace(',', '，')
        # # 评论内容
        # comment = item['content'].strip().replace('\n', '').replace(',', '，')
        # # 评论ID
        # comment_id = str(item['commentId'])
        # # 评论点赞数
        # praise = str(item['likedCount'])
        # # 评论时间
        # date = time.localtime(int(str(item['time'])[:10]))
        # date = time.strftime("%Y-%m-%d %H:%M:%S", date)
        # print(user_name, user_id, user_age, user_gender, user_city, user_introduce, comment, comment_id, praise, date)

        # with open('music_comments.csv', 'a', encoding='utf-8-sig') as f:
        #     f.write(user_name + ',' + user_id + ',' + user_age + ',' + user_gender + ',' + user_city + ',' + user_introduce + ',' + comment + ',' + comment_id + ',' + praise + ',' + date + '\n')
        # f.close()

        print()


def get_user(user_id):
    """
    获取用户注册时间
    """
    data = {}
    url = 'https://music.163.com/api/v1/user/detail/' + str(user_id)

    req = request.Request(url, headers=headers)  #使用request封装url和头部信息
    response = request.urlopen(req)     # 请求页面

    # 将页面数据转为json格式
    content_json = json.loads(response.read().decode("utf-8"))

    # 成功返回
    if content_json['code'] == 200:

        # 性别
        data['gender'] = content_json['profile']['gender']

        # 年龄
        if int(content_json['profile']['birthday']) < 0:
            data['age'] = 0
        else:
            data['age'] = (2018 - 1970) - (int(content_json['profile']['birthday']) // (1000 * 365 * 24 * 3600))
        
        if int(data['age']) < 0:
            data['age'] = 0

        # 城市
        data['city'] = content_json['profile']['city']

        # 个人介绍
        data['sign'] = content_json['profile']['signature']

    else:

        data['gender'] = '无'
        data['age'] = '无'
        data['city'] = '无'
        data['sign'] = '无'

    return data


get_comments(0)