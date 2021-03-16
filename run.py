import os
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


@app.route("/result")
def result(query):
    game_list = open("game-list.txt", "r").read().lower().split("\n")
    game_list.sort()
    results = []
    response = ""
    is_red = True
    for i in range(0, len(game_list)):
        if query.lower() in game_list[i]:
            results.append(game_list[i])

    if len(results) == 0:
        response = response+"<div class='result-div'><p>What you have entered is unable to find any matching website</p></div>"
    else:
        response = response+"<span>You have "+str(len(results))+" results.</span>"    
    for i in range(0, len(results)):
        if is_red:
            response = response+"<div class='result-div'><a class='red' href='"+str(results[i].lower().replace(" ", "_"))+"' >"+results[i].title()+"</a></div>"
            is_red = False
        else:
            response = response+"<div class='result-div'><a class='blue' href='"+str(results[i].lower().replace(" ", "_"))+"' >"+results[i].title()+"</a></div>"
            is_red = True
    return render_template("result.html", insert=response)


@app.route("/the_legend_of_zelda_ocarina_of_time")
def process():
    return render_template("the_legend_of_zelda_ocarina_of_time.html")


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True)