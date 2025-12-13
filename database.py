import sqlite3


class Database:
    def __init__(self, db_path="users.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row   # 讓資料可以用 dict 方式存取
        self.cursor = self.conn.cursor()
        self.init_tables()

    # ================== 初始化資料表 ==================
    def init_tables(self):
        # 使用者資料表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')

        # 留言資料表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                movie_id TEXT NOT NULL,
                username TEXT NOT NULL,
                comment TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # ⭐ 評分資料表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ratings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                movie_id TEXT NOT NULL,
                username TEXT NOT NULL,
                rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (movie_id, username)
            )
        ''')

        self.conn.commit()

    # ================== 使用者相關 ==================
    def add_user(self, username, password):
        try:
            self.cursor.execute(
                'INSERT INTO users (username, password) VALUES (?, ?)',
                (username, password)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def check_user(self, username, password):
        self.cursor.execute(
            'SELECT * FROM users WHERE username=? AND password=?',
            (username, password)
        )
        return self.cursor.fetchone()

    def get_user_by_username(self, username):
        self.cursor.execute(
            'SELECT * FROM users WHERE username=?',
            (username,)
        )
        return self.cursor.fetchone()

    # ================== 留言相關 ==================
    def add_comment(self, movie_id, username, comment):
        self.cursor.execute(
            'INSERT INTO comments (movie_id, username, comment) VALUES (?, ?, ?)',
            (movie_id, username, comment)
        )
        self.conn.commit()

    def get_comments(self, movie_id):
        self.cursor.execute(
            'SELECT * FROM comments WHERE movie_id = ? ORDER BY timestamp DESC',
            (movie_id,)
        )
        return self.cursor.fetchall()

    # ================== 評分相關 ==================
    # 新增或更新評分（同一使用者對同一電影只會有一筆）
    def add_or_update_rating(self, movie_id, username, rating):
        self.cursor.execute(
            '''
            INSERT INTO ratings (movie_id, username, rating)
            VALUES (?, ?, ?)
            ON CONFLICT(movie_id, username)
            DO UPDATE SET rating = excluded.rating
            ''',
            (movie_id, username, rating)
        )
        self.conn.commit()

    # 取得某部電影的平均評分
    def get_average_rating(self, movie_id):
        self.cursor.execute(
            'SELECT AVG(rating) AS avg_rating FROM ratings WHERE movie_id = ?',
            (movie_id,)
        )
        row = self.cursor.fetchone()
        if row['avg_rating'] is None:
            return None
        return round(row['avg_rating'], 1)
