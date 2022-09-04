import sys
sys.path.append("db_orm")
from db_orm.crud import *

import json, time
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/check", methods = ["GET", "POST"])
def check():
    user_name = request.form["user_name"]
    password = request.form["password"]
    account = get_account(user_name = user_name, password = password)
    if account:
        global login_account
        login_account = {
            "id": account.id, 
            "user_name": account.user_name, 
            "password": account.password, 
        }
        schedules = get_all_schedule() if get_all_schedule() else None
        return render_template("schedule.html", schedules = schedules)
    return redirect(url_for("login"))

@app.route("/sign_up")
def sign_up():
    return render_template("sign_up.html")

@app.route("/create_account", methods = ["GET", "POST"])
def create_account():
    user_name = json.loads(request.get_data())["user_name"]
    password = json.loads(request.get_data())["password"]
    if min(len(user_name), len(password)) == 0:
        return json.dumps("用戶名或密碼不得為空！(´・ω・｀)")
    account = get_account(user_name = user_name, password = password)
    if account:
        return json.dumps("該用戶已存在！( ﾟДﾟ)( ﾟДﾟ)( ﾟДﾟ)")
    insert_account(user_name = user_name, password = password)
    return redirect(url_for("login"))

@app.route("/write_schedule", methods = ["GET", "POST"])
def write_schedule():
    title = request.form["title"] if len(request.form["title"]) > 0 else "無標題"
    content = request.form["content"] if len(request.form["content"]) > 0 else "無內容"
    insert_schedule(user_name = login_account["user_name"], title = title, content = content)
    schedules = get_all_schedule()
    return render_template("schedule.html", schedules = schedules)
         
@app.route("/del_schedule", methods = ["GET", "POST"])
def del_schedule():
    schedule_id = json.loads(request.get_data())["id"]
    schedule = get_schedule(schedule_id = schedule_id)
    if (login_account["user_name"] == schedule.user_name):
        delete_schedule(schedule_id = schedule_id)
        schedules = get_all_schedule()
        return json.dumps("match")
    return json.dumps("no match")
    
if __name__ == "__main__":
    app.run(debug = True)