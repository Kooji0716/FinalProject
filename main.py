from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import Database

app = Flask(__name__)
app.secret_key = "your_secret_key"

db = Database()  #資料庫處理

#註冊路由
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if db.add_user(username, password):
            # 註冊成功
            return '''
                <script>
                    alert("註冊成功！");
                    window.location.href = "/login";
                </script>
            '''
        else:
            # 使用者名稱重複
            return '''
                <script>
                    alert("使用者名稱已經存在，請重新輸入");
                    window.location.href = "/register";
                </script>
            '''

    return render_template("register.html")



#登入路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = db.get_user_by_username(username)

        if user:
            if user['password'] == password:
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
                        alert("密碼錯誤，請確認後重新輸入！");
                        window.location.href = "/login";
                    </script>
                '''
        else:
            return '''
                <script>
                    alert("查無此帳號，請確認後重新輸入！");
                    window.location.href = "/login";
                </script>
            '''
    return render_template('login.html')


#登出路由
@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("已登出")
    return redirect(url_for("index"))

#首頁路由
@app.route("/")
def index():
    return render_template("index.html")

#各分頁路由
#恐怖片
@app.route("/horror")
def horror():
    return render_template("horror.html")
#喜劇
@app.route("/comedy")
def comedy():
    return render_template("comedy.html")
#科幻片
@app.route("/scifi")
def scifi():
    return render_template("scifi.html")
#愛情片
@app.route("/romance")
def romance():
    return render_template("romance.html")
#奇幻類
@app.route("/fantasy")
def fantasy():
    return render_template("fantasy.html")
#人生成長
@app.route("/life")
def life():
    return render_template("life.html")

#電影詳系頁面

#權力遊戲路由
#@app.route('/got')
#def got():
    return render_template('GOT.html')
#留言功能的電影詳細頁面
@app.route('/got', methods=['GET', 'POST'])
def got():
    if request.method == 'POST':
        if 'username' not in session:
            return '''
                <script>
                    alert("尚未登入，登入後即可留言！");
                    window.location.href = "/login";
                </script>
            '''
        username = session['username']
        comment = request.form.get('comment')
        if comment:
            db.add_comment('got', username, comment)
        return redirect(url_for('got'))

    comments = db.get_comments('got')
    return render_template('GOT.html', comments=comments)




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)


