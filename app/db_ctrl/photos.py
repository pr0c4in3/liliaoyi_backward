# db_ctrl/photos.py

import sqlite3

class Photos:
    def __init__(self, db_path='users.db'):
        self.conn = sqlite3.connect(db_path,check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        '''创建照片表'''
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS photos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nickname TEXT NOT NULL,
                photo_type INTEGER NOT NULL CHECK (photo_type IN (0, 1)),
                photo_path TEXT NOT NULL,
                FOREIGN KEY (nickname) REFERENCES users (username)
            )
        ''')
        self.conn.commit()

    def add_photo(self, nickname, photo_type, photo_path):
        '''添加照片信息'''
        try:
            self.cursor.execute('''
                INSERT INTO photos (nickname, photo_type, photo_path)
                VALUES (?, ?, ?)
            ''', (nickname, photo_type, photo_path))
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            print(f"Error adding photo: {e}")

    def delete_photo(self, nickname, photo_id):
        '''根据昵称和照片ID删除照片'''
        try:
            self.cursor.execute('DELETE FROM photos WHERE nickname = ? AND id = ?', (nickname, photo_id))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting photo: {e}")

    def update_photo(self, nickname, photo_id, photo_path=None, photo_type=None):
        '''根据昵称和照片ID更新照片信息'''
        updates = []
        params = ['nickname = ?', 'id = ?']
        if photo_path:
            updates.append('photo_path = ?')
            params.append(photo_path)
        if photo_type is not None:
            updates.append('photo_type = ?')
            params.append(photo_type)
        params.extend((nickname, photo_id))
        try:
            self.cursor.execute('''
                UPDATE photos
                SET %s
                WHERE nickname = ? AND id = ?
            ''' % ', '.join(updates), tuple(params))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error updating photo: {e}")

    def query_photos_by_nickname(self, nickname):
        '''根据昵称查询所有照片信息'''
        self.cursor.execute('SELECT * FROM photos WHERE nickname = ?', (nickname,))
        return self.cursor.fetchall()

    def __del__(self):
        self.conn.close()

# # 示例用法
# if __name__ == '__main__':
#     photos_manager = Photos()
#     # 添加照片
#     photos_manager.add_photo('Alice', 0, '/path/to/status_photo.jpg')
#     # 查询Alice的照片
#     photos = photos_manager.query_photos_by_nickname('Alice')
#     for photo in photos:
#         print(photo)
#     # 更新照片
#     photos_manager.update_photo('Alice', 1, photo_path='/path/to/new_photo.jpg')
#     # 删除照片
#     photos_manager.delete_photo('Alice', 1)