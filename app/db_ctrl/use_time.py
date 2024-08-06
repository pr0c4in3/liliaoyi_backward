# db_ctrl/use_time.py

import sqlite3
from datetime import datetime

class UseTime:
    def __init__(self, db_path='users.db'):
        self.conn = sqlite3.connect(db_path,check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        '''创建使用时长表'''
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS use_time (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nickname TEXT NOT NULL,
                use_duration INTEGER NOT NULL,  
                start_time TEXT NOT NULL,  
                FOREIGN KEY (nickname) REFERENCES users (username)
            )
        ''')
        # 使用时长，单位为分钟
        # 格式为 'YYYY-MM-DD HH:MM:SS'
        self.conn.commit()

    def add_use_time(self, nickname, use_duration, start_time):
        '''记录使用时长和开始时间'''
        try:
            self.cursor.execute('''
                INSERT INTO use_time (nickname, use_duration, start_time)
                VALUES (?, ?, ?)
            ''', (nickname, use_duration, start_time))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding use time: {e}")

    def update_use_time(self, nickname, use_duration, start_time):
        '''更新使用时长和开始时间'''
        try:
            self.cursor.execute('''
                UPDATE use_time
                SET use_duration = ?,
                    start_time = ?
                WHERE nickname = ?
            ''', (use_duration, start_time, nickname))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error updating use time: {e}")

    def query_use_time_by_nickname(self, nickname):
        '''根据昵称查询使用时长信息'''
        self.cursor.execute('SELECT use_duration, start_time FROM use_time WHERE nickname = ?', (nickname,))
        return self.cursor.fetchall()

    def delete_use_time(self, nickname):
        '''根据昵称删除使用时长信息'''
        try:
            self.cursor.execute('DELETE FROM use_time WHERE nickname = ?', (nickname,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting use time: {e}")

    def __del__(self):
        self.conn.close()

# # 示例用法
# if __name__ == '__main__':
#     use_time_manager = UseTime()
#     # 假设使用时长为3600秒，开始时间为当前时间
#     start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     use_time_manager.add_use_time('Alice', 3600, start_time)
#     # 查询Alice的使用时长
#     use_times = use_time_manager.query_use_time_by_nickname('Alice')
#     for use_time in use_times:
#         print(use_time)
#     # 更新使用时长
#     use_time_manager.update_use_time('Alice', 7200, start_time)
#     # 删除Alice的使用时长信息
#     use_time_manager.delete_use_time('Alice')