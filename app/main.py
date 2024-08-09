import os

#from flask import Flask
from flask import Flask, request, jsonify, session, send_from_directory, send_file, render_template
from login import LoginManager  # 导入登录类
from db_ctrl.users import Users
from db_ctrl.photos import Photos
from db_ctrl.info import Info
from db_ctrl.use_time import UseTime
from werkzeug.utils import secure_filename
from datetime import datetime


# 保存照片并返回编号
def save_photo(file, nickname, photo_type):
    filename = secure_filename(f"{nickname}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{file.filename.split('.')[-1]}")
    file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
    return filename





app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'photos'


users=Users()
photos=Photos()
info=Info()
usetime=UseTime()
# 初始化用户数据库


# 将LoginManager实例化并注册到app
login_manager = LoginManager()
login_manager.register(app)


my_url= 'http://6401f344.r3.cpolar.cn/'
photo_api='photo/'
dot='.'


@app.route('/del_pic', methods=['POST']) # 管理用户图片
def del_pic():
    data =request.get_json()
    print('删除的是：',data)
    photos.delete_photo_by_path(data['photo_id'])
    return jsonify({
            'success': True,
        })


@app.route('/manage_pic') # 管理用户图片
def manage_pic():
    return render_template('manage_pic.html')


@app.route('/changeNote', methods=['POST']) # 提交用户信息
def changeNote():
    data =request.get_json()
    # print(data)
    info.update_info(nickname=data['nickname'],doctor_notes=data['doctor_notes'])
    return jsonify({
            'success': True,
        })


@app.route('/getAll')  #后台管理显示所有用户
def getAll():
    res=info.show_all()
    formatted_records = [
        {"id": id, "nickname": nickname, "name": name, "gender": gender, "birthday": birthday, "phone": phone, "doctor_notes": doctor_notes}
        for id, nickname, name, gender, birthday, phone, doctor_notes in res
    ]
    print(formatted_records)
    # 返回JSON格式的响应
    return jsonify(formatted_records)


@app.route('/back')
def back():
    return render_template('back.html')

@app.route('/')
def hello_world():
    return '你好'


@app.route('/photo/<string:photo_id>', methods=['GET'])
def get_photo(photo_id):
    print(photo_id)
    now= os.path.join(os.getcwd(), 'photos')
    res= os.path.join(now,photo_id)
    # print(send_file(res, as_attachment=True))
    return send_file(res, as_attachment=True)


@app.route('/getPhoto', methods=['POST'])
def getPhoto():
    data =request.get_json()
    nickname=data['nickname']
    res_photos=photos.query_photos_by_nickname(nickname)
    photos_path = [res_photo[3] for res_photo in res_photos]
    for index, item in enumerate(photos_path):
        photos_path[index] = my_url + photo_api + item 
    return jsonify(photos=photos_path)
    


@app.route('/upload', methods=['POST'])
def upload_file():
    print(request.files)
    if 'photo' not in request.files:
        print('无文件')
        return jsonify({'error': '没有文件部分'})
    file = request.files['photo']
    if file.filename == '':
        print('没有选择文件')
        return jsonify({'error': '没有选择文件'})
    if file:
        nickname = request.form.get('nickname')
        print(nickname)
        #photo_type = request.form.get('photo_type')
        photo_path = save_photo(file, nickname, 0)
        print(photo_path)
        photos.add_photo(nickname, 0, photo_path)
        return jsonify({'message': '文件上传成功', 'success': True, 'photo_path': photo_path})



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
        info.update_info(nickname=data['nickname'],name=data['name'],gender=data['gender'],birthday=data['birthday'],phone=data['phone'],doctor_notes='暂无')
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