import os
import json
from flask import Flask, render_template, request

app = Flask(__name__)
user_id = {
    "username": "warr",
    "passw": "test",
}
g_error_msg = 0


@app.route("/")
def index():
    return render_template("index.html", user=user_id)


@app.route("/signout")
def signout():
    global user_id
    user_id = ""
    return login()


@app.route("/login")
def login():
    if user_id == "":
        return render_template(
            "login.html", user=user_id, error_message=g_error_msg)
    else:
        return index()


@app.route("/account")
def account():
    return render_template("account.html", user=user_id)


@app.route("/singin", methods=["POST"])
def signin():
    error_msg = 0
    action = request.form.get("Submit")
    usern = request.form.get("Username")
    passw = request.form.get("Passw")
    user_auth = False
    if action == "login":
        user_auth = False
    elif action == "signup":
        user_auth = True
    if not testFile("data/users.json"):
        return error()
    with open("data/users.json", "r") as users:
        file = json.load(users)
        for i in range(len(file)):
            if action == "login":
                if usern == file[i]["username"]:
                    if passw == file[i]["passw"]:
                        user_auth = True
                        global user_id
                        user_id = file[i]
                    else:
                        error_msg = 1
                else:
                    error_msg = 2
            elif action == "signup":
                if usern == file[i]["username"]:
                    user_auth = False
                    error_msg = 3
        if user_auth is True and action == "login":
            return account()
        elif user_auth is True and action == "signup":
            with open("data/users.json", "r") as raw_file:
                file = json.load(raw_file)
                user_id = {
                    "username": usern,
                    "passw": passw
                }
                with open("data/users.json", "w") as users:
                    file.append(user_id)
                    json.dump(file, users, indent=3)
            return account()
        else:
            global g_error_msg
            g_error_msg = error_msg
            error_msg = 0
            passw = ""
            return login()


@app.route("/inquire")
def inquire():
    return render_template("page_inquiry.html", user=user_id)


@app.route("/post", methods=["POST"])
def post():
    title = request.form.get("Title")
    console = request.form.get("Console")
    detail = request.form.get("Details")
    with open("data/game-log.json", "r") as games:
        game_log = json.load(games)
        add_game = True
        for i in range(len(game_log)):
            if title == game_log[i]["name"]:
                add_game = False
        if add_game:
            with open("data/game-log.json", "w") as game_file:
                new_log = {
                    "name": title,
                    "series": title,
                    "console": console,
                    "details": detail,
                    "link": str(title).lower().replace(" ", "_"),
                    "game_title": [

                    ],
                    "comment_title": [
                    ],
                    "comment_tag": [
                    ],
                    "comment": [
                    ],
                    "author": [
                    ],
                    "num_comments": 0,
                    "page_creater": user_id["username"]
                }
                game_log.append(new_log)
                json.dump(game_log, game_file, indent=3)
                creditor(title, user_id["username"], title, detail, "page")
        return index()


@app.route("/search", methods=["POST"])
def search():
    text = request.form.get("Search")
    return result(text)


def error():
    return render_template("error.html", user=user_id)


def result(query):
    file = []
    results = []
    if not testFile("data/game-log.json"):
        return error()
    with open("data/game-log.json", "r") as games_data:
        file = json.load(games_data)
        for i in range(len(file)):
            if query.lower() in file[i]["name"].lower():
                results.append(file[i])
        num = len(results)
        if num == 0:
            return inquire()
        return render_template(
            "result.html", results=results, num_search=num, query=query, user=user_id)


@app.route("/<game_name>", methods=["POST", "GET"])
def page_load(game_name):
    if request.method == "POST":
        if len(user_id) > 0:
            title = request.form.get("Title")
            tag = request.form.get("Radio")
            detail = request.form.get("Details")
            commentWrite(
                game_name, user_id["username"], title, detail, tag)
    file = []
    with open("data/game-log.json", "r") as games_data:
        file = json.load(games_data)
        for obj in file:
            if obj["link"] == game_name:
                game = obj
                if obj["series"] in obj["name"]:
                    red = obj["series"]
                    blue = obj["name"][len(obj["series"]):len(obj["name"])]
                else:
                    red = obj["name"]
    return render_template(
        "page_template.html", game=game, red=red, blue=blue, user=user_id)


def commentWrite(game_name, usern, title, comment, tag):
    with open("data/game-log.json", "r") as games:
        game_log = json.load(games)
        for i in range(len(game_log)):
            if game_name == game_log[i]["link"] and comment not in game_log[i]["comment"]:
                game_log[i]["comment_title"].append(title)
                game_log[i]["comment_tag"].append(tag)
                game_log[i]["comment"].append(comment)
                game_log[i]["author"].append(usern)
                game_log[i]["num_comments"] = game_log[i]["num_comments"]+1
        with open("data/game-log.json", "w") as file:
            json.dump(game_log, file, indent=3)
    creditor(game_name, usern, title, comment, tag)


def creditor(game_name, usern, title, comment, tag):
    with open("data/users.json", "r") as users:
        user_log = json.load(users)
        for i in range(len(user_log)):
            if usern == user_log[i]["username"] and comment not in user_log[i]["comment"]:
                user_log[i]["game_title"].append(game_name)
                user_log[i]["comment_title"].append(title)
                user_log[i]["comment_tag"].append(tag)
                user_log[i]["comment"].append(comment)
                user_log[i]["num_comments"] = user_log[i]["num_comments"]+1
        with open("data/users.json", "w") as file:
            json.dump(user_log, file, indent=3)


def testFile(file):
    try:
        open(file, "r")
        return True
    except Exception:
        return False


if __name__ == "__main__":
    app.run(
        host=os.environ.get(
            "IP", "0.0.0.0"), port=int(
                os.environ.get("PORT", "5000")), debug=True)