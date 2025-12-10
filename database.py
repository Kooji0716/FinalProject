import sqlite3


class Database:
    def __init__(self, db_path="users.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row   # 讓資料可以用 dict 方式存取
        self.cursor = self.conn.cursor()
        self.init_tables()

    # 初始化資料表
    def init_tables(self):
        # 使用者資料表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')

        # 留言資料表（電影詳細頁使用）
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                movie_id TEXT NOT NULL,
                username TEXT NOT NULL,
                comment TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        self.conn.commit()

    # ========== 使用者相關 ==========
    # 註冊新使用者
    def add_user(self, username, password):
        try:
            self.cursor.execute(
                'INSERT INTO users (username, password) VALUES (?, ?)',
                (username, password)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            # username 重複（因為 UNIQUE 限制）
            return False

    # 直接檢查帳號密碼（登入用）
    def check_user(self, username, password):
        self.cursor.execute(
            'SELECT * FROM users WHERE username=? AND password=?',
            (username, password)
        )
        return self.cursor.fetchone()

    # 只用帳號搜尋（判斷帳號是否存在）
    def get_user_by_username(self, username):
        self.cursor.execute(
            'SELECT * FROM users WHERE username=?',
            (username,)
        )
        return self.cursor.fetchone()

    # ========== 留言相關 ==========
    # 新增留言
    def add_comment(self, movie_id, username, comment):
        self.cursor.execute(
            'INSERT INTO comments (movie_id, username, comment) VALUES (?, ?, ?)',
            (movie_id, username, comment)
        )
        self.conn.commit()

    # 取得某部電影的所有留言
    def get_comments(self, movie_id):
        self.cursor.execute(
            'SELECT * FROM comments WHERE movie_id = ? ORDER BY timestamp DESC',
            (movie_id,)
        )
        return self.cursor.fetchall()
