import os
import json
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/search", methods=["POST"])
def search():
    text = request.form.get("Search")
    return result(text)


def result(query):
    file = []
    results = []
    with open("data/game-log.json", "r") as games_data:
        file = json.load(games_data)
        for i in range(len(file)):
            if query.lower() in file[i]["name"].lower():
                results.append(file[i])
        num = len(results)
        if num == 0:
            return render_template("page_inquiry.html", query=query)
        return render_template(
            "result.html", results=results, num_search=num, query=query)


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
    return render_template("page_template.html", game=game, red=red, blue=blue)


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"), 
        port=int(os.environ.get("PORT", "5000")), 
        debug=True)