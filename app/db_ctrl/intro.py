import sqlite3

class Intro:
    def __init__(self, db_name='intro.db'):
        self.conn = sqlite3.connect(db_name,check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS introductions (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def add_introduction(self, title, content):
        self.cursor.execute('''
            INSERT INTO introductions (title, content) VALUES (?, ?)
        ''', (title, content))
        self.conn.commit()

    def get_all_introductions(self):
        self.cursor.execute('SELECT * FROM introductions')
        return self.cursor.fetchall()

    def update_introduction(self, id, title, content):
        self.cursor.execute('''
            UPDATE introductions SET title = ?, content = ? WHERE id = ?
        ''', (title, content, id))
        self.conn.commit()

    def delete_introduction(self, id):
        self.cursor.execute('DELETE FROM introductions WHERE id = ?', (id,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()


    