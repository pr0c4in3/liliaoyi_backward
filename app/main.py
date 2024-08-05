import os

#from flask import Flask
from flask import Flask, request, jsonify
from login import LoginManager  # 导入登录类

app = Flask(__name__)

# 将LoginManager实例化并注册到app
login_manager = LoginManager()
login_manager.register(app)


@app.route('/')
def hello_world():
    return '欢迎使用微信云托管！'


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 80)))