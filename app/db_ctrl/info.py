# db_ctrl/info.py

import sqlite3

class Info:
    def __init__(self, db_path='users.db'):
        self.conn = sqlite3.connect(db_path,check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        '''创建用户信息表'''
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nickname TEXT NOT NULL,
                name TEXT NOT NULL,
                gender TEXT NOT NULL,
                birthday DATE,
                phone TEXT,
                doctor_notes TEXT,
                FOREIGN KEY (nickname) REFERENCES users (username)
            )
        ''')
        self.conn.commit()

    def add_info(self, nickname, name, gender, birthday, phone, doctor_notes):
        '''添加用户信息'''
        self.cursor.execute('''
            INSERT INTO info (nickname, name, gender, birthday, phone, doctor_notes) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nickname, name, gender, birthday, phone, doctor_notes))
        self.conn.commit()

    def delete_info(self, nickname):
        '''根据昵称删除用户信息'''
        self.cursor.execute('DELETE FROM info WHERE nickname = ?', (nickname,))
        self.conn.commit()

    def update_info(self, nickname, name=None, gender=None, birthday=None, phone=None, doctor_notes=None):
        '''根据昵称更新用户信息'''
        updates = []
        params = []
        if name:
            updates.append('name = ?')
            params.append(name)
        if gender:
            updates.append('gender = ?')
            params.append(gender)
        if birthday:
            updates.append('birthday = ?')
            params.append(birthday)
        if phone:
            updates.append('phone = ?')
            params.append(phone)
        if doctor_notes:
            updates.append('doctor_notes = ?')
            params.append(doctor_notes)
        if updates:
            params.append(nickname)
            update_query = 'UPDATE info SET ' + ', '.join(updates) + ' WHERE nickname = ?'
            try:
                print(update_query,params)
                self.cursor.execute(update_query, params)
                self.conn.commit()
                print("修改完成")
            except Exception as e:
            # 这里可以添加更详细的错误处理逻辑
                print(f"An error occurred: {e}")
            # 回滚事务
                self.conn.rollback()

    def query_info_by_nickname(self, nickname):
        '''根据昵称查询用户信息'''
        self.cursor.execute('SELECT * FROM info WHERE nickname = ?', (nickname,))
        return self.cursor.fetchone()

    def __del__(self):
        self.conn.close()

    def show_all(self):
        self.cursor.execute('SELECT * FROM info ',)
        return self.cursor.fetchall()
    

# info_manager = Info()
# info_manager.update_info(nickname='微信用户',doctor_notes='1')
# print(info_manager.show_all())

# # 示例用法
# if __name__ == '__main__':
#     info_manager = Info()
#     # 添加用户信息
#     info_manager.add_info('Alice', 'Alice Smith', 'Female', '1990-01-01', '1234567890', 'Patient has a history of...')
#     # 查询Alice的信息
#     info = info_manager.query_info_by_nickname('Alice')
#     print(info)
#     # 更新用户信息
#     info_manager.update_info('Alice', phone='0987654321')
#     # 删除用户信息
#     info_manager.delete_info('Alice')