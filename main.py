from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import Database

app = Flask(__name__)
app.secret_key = "your_secret_key"

db = Database()  #資料庫處理

@app.route("/")
def index():
    return render_template("index.html")

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



@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("已登出")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
