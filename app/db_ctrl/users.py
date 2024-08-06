# db_ctrl/users.py

import sqlite3

class Users:
    def __init__(self, db_path='users.db'):
        self.conn = sqlite3.connect(db_path,check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        '''创建用户表'''
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nickname TEXT NOT NULL,
                avatar_url TEXT,
                gender TEXT
            )
        ''')
        self.conn.commit()

    def add_user(self, nickname, avatar_url, gender):
        '''添加用户'''
        self.cursor.execute('INSERT INTO users (nickname, avatar_url, gender) VALUES (?, ?, ?)',
                             (nickname, avatar_url, gender))
        self.conn.commit()

    def delete_user(self, nickname):
        '''根据用户名删除用户'''
        self.cursor.execute('DELETE FROM users WHERE nickname = ?', (nickname,))
        self.conn.commit()

    def update_user(self, nickname, avatar_url=None, gender=None):
        '''根据用户名更新用户信息'''
        updates = []
        params = []
        if avatar_url:
            updates.append('avatar_url = ?')
            params.append(avatar_url)
        if gender:
            updates.append('gender = ?')
            params.append(gender)
        params.append(nickname)
        self.cursor.execute('UPDATE users SET ' + ', '.join(updates) + ' WHERE nickname = ?',
                             params)
        self.conn.commit()

    def query_user(self, nickname):
        '''根据用户名查询用户信息'''
        self.cursor.execute('SELECT * FROM users WHERE nickname = ?', (nickname,))
        user = self.cursor.fetchone()
        return user

    def __del__(self):
        self.conn.close()
    
    def query_all_users(self):
        '''查询所有用户信息'''
        self.cursor.execute('SELECT * FROM users')
        return self.cursor.fetchall()


# # 以下为示例用法
# if __name__ == '__main__':
#     users_manager = Users()
#     # 添加用户
#     users_manager.add_user('Alice', 'http://example.com/avatar.jpg', 'Female')
#     # 查询用户
#     user_info = users_manager.query_user('Alice')
#     print(user_info)
#     # 更新用户
#     users_manager.update_user('Alice', gender='Male')
#     # 删除用户
#     users_manager.delete_user('Alice')