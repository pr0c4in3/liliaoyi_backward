# db_ctrl/db_manager.py

import sqlite3

class DbManager:
    def __init__(self, db_path='users.db'):
        self.conn = sqlite3.connect(db_path,check_same_thread=False)
        self.cursor = self.conn.cursor()

    def show_tables(self):
        '''显示数据库中的所有表'''
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cursor.fetchall()
        return [table[0] for table in tables]

    def __del__(self):
        self.conn.close()

# 示例用法
if __name__ == '__main__':
    db_manager = DbManager()
    # 显示数据库中的所有表
    tables = db_manager.show_tables()
    print("Database tables:", tables)