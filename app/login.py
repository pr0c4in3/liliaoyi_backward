from flask import Flask, request, jsonify
import uuid
import os
import json
import requests


class LoginManager:
    # 微信小程序的appid和secret
    APPID = 'wx71fb27fab2efa872'
    SECRET = '05a1ef2809036feb21f928f51d2b193e'
    # 从小程序前端获取的code
    js_code = '从小程序前端获取的js_code'

    # 微信接口的基础URL
    BASE_URL = 'https://api.weixin.qq.com/sns/jscode2session'

    

    def __init__(self):
        self.logged_users = {}  # 存储已登录用户的信息

    def login(self):
        
        # 获取请求中的code
        code = request.json.get('code')
        if not code:
            return jsonify({'success': False, 'message': '缺少必要的code参数'}), 400

        # 这里应该调用微信的API，使用code换取session_key和openid
        # 假设我们已经有了openid和session_key，这里直接生成模拟数据
        self.js_code=code
            # 构建请求的完整URL
        url = f"{self.BASE_URL}?appid={self.APPID}&secret={self.SECRET}&js_code={self.js_code}&grant_type=authorization_code"
        # 发送GET请求
        response = requests.get(url)

                # 检查请求是否成功
        if response.status_code == 200:
            # 解析返回的JSON数据
            result = response.json()
            # 检查微信接口是否返回了错误
            if result.get('errcode'):
                print(f"微信接口错误：{result.get('errmsg')}")
                return f"微信接口错误：{result.get('errmsg')}"
            else:
                # 正常返回，打印session_key和openid
                session_key = result.get('session_key')
                openid = result.get('openid')
                print(f"Session Key: {session_key}, OpenID: {openid}")
        else:
            print(f"请求失败，状态码：{response.status_code}")

        # openid = str(uuid.uuid4())  # 模拟的openid
        # session_key = str(uuid.uuid4())  # 模拟的session_key

        # 假设我们已经有了用户信息，这里直接返回
        # user_info = {
        #     'nickName': '测试用户',
        #     'avatarUrl': 'https://example.com/avatar.jpg'
        # }

        # 存储登录状态
        # self.logged_users[openid] = user_info

        return jsonify({
            'success': True,
        })

    def register(self, app):
        # 将登录路由添加到Flask应用中
        app.add_url_rule('/login', view_func=self.login, methods=['POST'])