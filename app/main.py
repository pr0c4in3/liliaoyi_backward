import os

#from flask import Flask
from flask import Flask, request, jsonify, session
from login import LoginManager  # 导入登录类
from db_ctrl.users import Users
from db_ctrl.photos import Photos
from db_ctrl.info import Info
from db_ctrl.use_time import UseTime


app = Flask(__name__)
app.secret_key = 'your_secret_key'

users=Users()
photos=Photos()
info=Info()
usetime=UseTime()
# 初始化用户数据库


# 将LoginManager实例化并注册到app
login_manager = LoginManager()
login_manager.register(app)





@app.route('/')
def hello_world():
    return '欢迎使用微信云托管！'


@app.route('/getUserInfo', methods=['POST']) # 获取用户信息
def getUserInfo():
    data =request.get_json()
    nickname=data['nickname']
    answer= info.query_info_by_nickname(nickname)
    res={"name":answer[2],"gender":answer[3],"birthday":answer[4],"phone":answer[5],"doctor_notes":answer[6]}
    # 返回JSON格式的响应
    return jsonify(res)



@app.route('/submitInfo', methods=['POST']) # 提交用户信息
def submitInfo():
    data =request.get_json()
    if(info.query_info_by_nickname(data['nickname'])==None):
        print('提交信息')
        info.add_info(nickname=data['nickname'],name=data['name'],gender=data['gender'],birthday=data['birthday'],phone=data['phone'],doctor_notes='暂无')
    else:
        print('修改信息')
        info.delete_info(nickname=data['nickname'])
        info.add_info(nickname=data['nickname'],name=data['name'],gender=data['gender'],birthday=data['birthday'],phone=data['phone'],doctor_notes='暂无')
    #print(data)
    return jsonify({
            'success': True,
        })

@app.route('/getUseTime', methods=['POST'])
def getusetime():
    data =request.get_json()
    nickname=data['nickname']
    answer= usetime.query_use_time_by_nickname(nickname)
    # print(answer)
    formatted_records = [
        {"startTime": start_time, "duration": use_duration}
        for use_duration, start_time in answer
    ]
    print(formatted_records)
    # 返回JSON格式的响应
    return jsonify(formatted_records)

@app.route('/timer', methods=['POST'])
def receive_use_time():
    data =request.get_json()
    nickname=data['userName']
    duration=data['duration']
    startTime=data['startTime']
    usetime.add_use_time(nickname,int(duration),startTime)
    # print('search:',usetime.query_use_time_by_nickname('微信用户'))
    return jsonify({
            'success': True,
        })



@app.route('/user', methods=['POST'])
def receive_user_info():
    # 获取JSON请求数据
    data = request.get_json()
    
    # 打印接收到的用户信息
    print(data)
    
    user_nickname = data.get('userInfo', {}).get('nickName', 'Unknown User')
    user_gender = data.get('userInfo', {}).get('gender', 'Unknown User')
    user_avatarUrl = data.get('userInfo', {}).get('avatarUrl', 'Unknown User')
    # 将用户信息检索并存入数据库
    if (users.query_user(user_nickname)==None):
        users.add_user(user_nickname,user_avatarUrl,user_gender)
    else:
        print('该用户已存在')


    
    print(user_nickname)
    session['username']=user_nickname
    # 返回响应给客户端
    return jsonify({
        'message': 'User info received',
        'yourNickname': user_nickname
    })



if __name__ == "__main__":
    # app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 80)))
    app.run(debug=True,host='127.0.0.1',port=int(os.environ.get('PORT', 8080)))