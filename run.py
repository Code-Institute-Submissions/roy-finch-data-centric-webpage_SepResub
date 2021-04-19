import os
import json
from flask import Flask, render_template, request

app = Flask(__name__)
user_id = ""
error_msg = False


@app.route("/")
def index():
    return render_template("index.html", user=user_id)


@app.route("/signout")
def signout():
    global user_id
    user_id = ""
    return login()


@app.route("/<game_name>/comment", methods=["POST"])
def add_comment(game_name):
    if user_id != "":
        title = request.form.get("Title")
        tag = request.form.get("Radio")
        detail = request.form.get("Details")
        user = user_id["username"]
        return game_name+" "+title+" "+tag+" "+detail+" "+user


@app.route("/login")
def login():
    if user_id == "":
        return render_template(
            "login.html", user=user_id, error_message=error_msg)
    else:
        return index()


@app.route("/account")
def account():
    return render_template("account.html", user=user_id)


@app.route("/singin", methods=["POST"])
def signin():
    action = request.form.get("Submit")
    email = request.form.get("Email")
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
                        if email == file[i]["email"]:
                            user_auth = True
                            global user_id
                            user_id = file[i]
            elif action == "signup":
                if usern != file[i]["username"]:
                    user_auth = False
                if email != file[i]["email"]:
                    user_auth = False
        if user_auth is True:
            return index()
        else:
            return login()


@app.route("/inquire")
def inquire():
    return render_template("page_inquiry.html", user=user_id)


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


@app.route("/<game_name>")
def page_load(game_name):
    file = []
    with open("data/game-log.json", "r") as games_data:
        file = json.load(games_data)
        for obj in file:
            if obj["link"] == game_name:
                game = obj
                if obj["series"] not in obj["name"]:
                    red = obj["name"][0:round(len(obj["name"])/2)]
                    blue = obj["name"][round(len(
                        obj["name"])/2):len(obj["name"])]
                else:
                    red = obj["series"]
                    blue = obj["name"][len(obj["series"]):len(obj["name"])]
    return render_template(
        "page_template.html", game=game, red=red, blue=blue, user=user_id)


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