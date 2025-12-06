from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import Database

app = Flask(__name__)
app.secret_key = "your_secret_key"

db = Database()  # ← 全部資料庫操作只用這個

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if db.add_user(username, password):
            flash("註冊成功！")
            return redirect(url_for("index"))
        else:
            flash("使用者名稱已存在！")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = db.check_user(username, password)

        if user:
            session["username"] = username
            return '''
                <script>
                    alert("登入成功！");
                    window.location.href = "/";
                </script>
            '''
        else:
            flash("登入失敗：帳號或密碼錯誤")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("已登出")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
