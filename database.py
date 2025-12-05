# database.py
import sqlite3

class Database:
    def __init__(self, db_path="users.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.init_tables()

    def init_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def add_user(self, username, password):
        try:
            self.cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            self.conn.commit()
            return True  # 註冊成功
        except sqlite3.IntegrityError:
            return False  # 使用者名稱已存在
