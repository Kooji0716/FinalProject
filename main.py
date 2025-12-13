from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import Database

app = Flask(__name__)
app.secret_key = "your_secret_key"

db = Database()

# ======================
# 註冊
# ======================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if db.add_user(username, password):
            return '''
                <script>
                    alert("註冊成功！");
                    window.location.href = "/login";
                </script>
            '''
        else:
            return '''
                <script>
                    alert("使用者名稱已經存在，請重新輸入");
                    window.location.href = "/register";
                </script>
            '''
    return render_template("register.html")


# ======================
# 登入
# ======================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = db.get_user_by_username(username)

        if user and user['password'] == password:
            session['username'] = username
            return '''
                <script>
                    alert("登入成功！");
                    window.location.href = "/";
                </script>
            '''
        else:
            return '''
                <script>
                    alert("帳號或密碼錯誤！");
                    window.location.href = "/login";
                </script>
            '''
    return render_template('login.html')


# ======================
# 登出
# ======================
@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("已登出")
    return redirect(url_for("index"))


# ======================
# 首頁與分類頁
# ======================
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/horror")
def horror():
    return render_template("horror.html")

@app.route("/comedy")
def comedy():
    return render_template("comedy.html")

@app.route("/scifi")
def scifi():
    return render_template("scifi.html")

@app.route("/romance")
def romance():
    return render_template("romance.html")

@app.route("/fantasy")
def fantasy():
    return render_template("fantasy.html")

@app.route("/life")
def life():
    return render_template("life.html")


# ======================
# 電影詳細頁：權力遊戲 + 留言
# ======================
@app.route('/got', methods=['GET', 'POST'])
def got():
    movie_id = 'got'

    if request.method == 'POST':
        if 'username' not in session:
            return '''
                <script>
                    alert("尚未登入，登入後即可留言與評分！");
                    window.location.href = "/login";
                </script>
            '''

        username = session['username']
        comment = request.form.get('comment')
        rating = request.form.get('rating')

        if comment:
            db.add_comment(movie_id, username, comment)

        if rating:  # 如果有送出評分
            try:
                rating = int(rating)
                db.add_or_update_rating(movie_id, username, rating)
            except ValueError:
                pass  # rating 不是整數就略過

        return redirect(url_for('got'))

    # GET 時查詢留言與平均評分
    comments = db.get_comments(movie_id)
    avg_rating = db.get_average_rating(movie_id)

    return render_template('GOT.html', comments=comments, avg_rating=avg_rating)

#星際校應路由
@app.route('/interstellar', methods=['GET', 'POST'])
def interstellar():
    movie_id = 'interstellar'

    if request.method == 'POST':
        if 'username' not in session:
            return '''
                <script>
                    alert("尚未登入，登入後即可留言與評分！");
                    window.location.href = "/login";
                </script>
            '''

        username = session['username']
        comment = request.form.get('comment')
        rating = request.form.get('rating')

        if comment:
            db.add_comment(movie_id, username, comment)

        if rating:
            db.add_or_update_rating(movie_id, username, int(rating))

        return redirect(url_for('interstellar'))

    comments = db.get_comments(movie_id)
    avg_rating = db.get_average_rating(movie_id)

    return render_template(
        'interstellar.html',
        comments=comments,
        avg_rating=avg_rating
    )


# ======================
# 啟動伺服器
# ======================
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
