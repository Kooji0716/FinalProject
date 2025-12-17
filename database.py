import sqlite3


class Database:
    def __init__(self, db_path="users.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.enable_foreign_keys()
        self.init_tables()

    def enable_foreign_keys(self):
        # ✅ 啟用 SQLite 的外鍵支援
        self.cursor.execute('PRAGMA foreign_keys = ON')

    # ================== 初始化資料表 ==================
    def init_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                movie_id TEXT NOT NULL,
                username TEXT NOT NULL,
                comment TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

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

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS community_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS community_comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER NOT NULL,
                username TEXT NOT NULL,
                comment TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (post_id) REFERENCES community_posts(id) ON DELETE CASCADE
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

    def add_community_comment(self, post_id, username, comment):
        self.cursor.execute(
            'INSERT INTO community_comments (post_id, username, comment) VALUES (?, ?, ?)',
            (post_id, username, comment)
        )
        self.conn.commit()

    def get_community_comments(self, post_id):
        self.cursor.execute(
            'SELECT * FROM community_comments WHERE post_id = ? ORDER BY timestamp ASC',
            (post_id,)
        )
        return self.cursor.fetchall()

    # ================== 評分相關 ==================
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

    def get_average_rating(self, movie_id):
        self.cursor.execute(
            'SELECT AVG(rating) AS avg_rating FROM ratings WHERE movie_id = ?',
            (movie_id,)
        )
        row = self.cursor.fetchone()
        if row['avg_rating'] is None:
            return None
        return round(row['avg_rating'], 1)

    # ================== 貼文操作 ==================
    def add_community_post(self, username, title, content):
        self.cursor.execute(
            'INSERT INTO community_posts (username, title, content) VALUES (?, ?, ?)',
            (username, title, content)
        )
        self.conn.commit()

    def get_all_community_posts(self):
        self.cursor.execute(
            'SELECT * FROM community_posts ORDER BY timestamp DESC'
        )
        return self.cursor.fetchall()

    def delete_community_post(self, post_id):
        self.cursor.execute(
            'DELETE FROM community_posts WHERE id = ?',
            (post_id,)
        )
        self.conn.commit()
    def get_post_by_id(self, post_id):
        self.cursor.execute(
            'SELECT * FROM community_posts WHERE id = ?',
            (post_id,)
        )
        return self.cursor.fetchone()
