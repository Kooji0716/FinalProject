from flask import Flask, render_template, request, redirect, url_for, flash
from database import Database

app = Flask(__name__)
app.secret_key = "your_secret_key"  # flash() 需要用
db = Database()

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

if __name__ == "__main__":
    app.run(debug=True)
