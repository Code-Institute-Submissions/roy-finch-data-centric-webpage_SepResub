import os
import json
from flask import (
    Flask, render_template, request, session, redirect, url_for
    )
from flask_login import (
    LoginManager, login_user, logout_user, current_user
    )
from model import User
# Set up the required variables needed
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret-key"
login_manager = LoginManager()
login_manager.init_app(app)
g_error_msg = 0


@login_manager.user_loader
def load_user(user_id):
    # This will get the user by there id
    return User.get(user_id)


@app.route("/")
def index():
    # This is the function for the homepage
    return render_template("index.html")


@app.route("/signout")
def signout():
    # This will signout the user then return them to login page.
    logout_user()
    session.pop("user_id", None)
    return login()


@app.route("/login")
def login():
    # Load up the login with a relavant error msg
    if "user_id" not in session:
        return render_template(
            "login.html", error_message=g_error_msg)
    else:
        return redirect({{url_for("index")}})


@app.route("/account")
def account():
    # This gets the user info and the renders the account page.
    if current_user is not None:
        user = userID(current_user)
        return render_template("account.html", user=user)
    else:
        redirect({{url_for("login")}})


@app.route("/singin", methods=["POST"])
def signin():
    # This is to deal with signing in or signing up
    session.pop("user_id", None)
    error_msg = 0
    # This get the information from the form
    action = request.form.get("Submit")
    usern = request.form.get("Username")
    passw = request.form.get("Passw")
    # This is a var to deal with if the info supplied is right.
    user_auth = False
    # This sets the user_auth value depending on the users action, signin/login
    if action == "login":
        user_auth = False
    elif action == "signup":
        user_auth = True
    # Test the file and check if it works or not
    if not testFile("data/users.json"):
        return error()
    # When the file works start to read to check the info against the supply
    with open("data/users.json", "r") as users:
        # Var file is opened and converted using json functions
        file = json.load(users)
        for i in range(len(file)):
            # Do two different functions depending on the actions of user
            if action == "login":
                if usern == file[i]["username"]:
                    if passw == file[i]["passw"]:
                        # Check users input against data in file.
                        user_auth = True
                        # Allow the user to pass and set up the session tag
                        session["user_id"] = file[i]["id"]
                        # Login the user and set the corrispoding values
                        login_user(User(
                            file[i]["id"], usern, passw, True, True))
                    else:
                        # Return error message about wrong password
                        error_msg = 1
                else:
                    # Return error message about wrong username
                    error_msg = 2
            elif action == "signup":
                # If the users action is signup do a diff action
                if usern == file[i]["username"]:
                    # If the username is checked and is equal
                    # Stop the user from continuing and read an error
                    user_auth = False
                    # Error msg 3, username is taken.
                    error_msg = 3
        if user_auth is True and action == "login":
            # This checks if they are allowed to continue
            # This then returns them to the homepage.
            return index()
        elif user_auth is True and action == "signup":
            # If the action is to signup do something different
            with open("data/users.json", "r") as raw_file:
                # Open user file to update the file with new user details
                file = json.load(raw_file)
                # Create a formate of the way data is presented
                # Id, used by the LoginManager
                # Username, username given by user
                # Password, given by the user
                # Initialize the other arrays and variabels
                # to edit them later.
                user_id = {
                    "id": len(file),
                    "username": usern,
                    "passw": passw,
                    "game_title": [
                    ],
                    "comment_title": [
                    ],
                    "comment_tag": [
                    ],
                    "comment": [
                    ],
                    "num_comments": 0
                }
                # Open the session["user_id"] and set the id to current user
                session["user_id"] = user_id["id"]
                # Set up the user as User model and add to the login_user()
                user = User(user_id["id"], usern, passw, True, False)
                login_user(user)
                # Open the user file and edit it as related
                with open("data/users.json", "w") as users:
                    # With the new information add it to the file
                    # Dump the new edited file and save.
                    file.append(user_id)
                    json.dump(file, users, indent=3)
            # Return to the index after they are added to the user file.
            return redirect({{url_for("index")}})
        else:
            # Set up the g_error_msg as global and output it for the
            # login page to use it.
            global g_error_msg
            g_error_msg = error_msg
            # Refresh the local error_msg after updating the global var
            error_msg = 0
            # Reset the password var
            passw = ""
            # Return the login page with the new error.
            return login()


@app.route("/inquire")
def inquire():
    # This is the inquire function to add a new page
    # If there is a game that you want but has no page.
    return render_template("page_inquiry.html")


@app.route("/post", methods=["POST"])
def post():
    # This is to post a comment
    # Take information from the form
    title = request.form.get("Title")
    console = request.form.get("Console")
    detail = request.form.get("Details")
    # Open the game-log and edit it as seen
    with open("data/game-log.json", "r") as games:
        # Open file and use json load to convert
        game_log = json.load(games)
        # Set a boolean to flag if it can't be added
        add_game = True
        for i in range(len(game_log)):
            if title == game_log[i]["name"]:
                # Check if the gamename is already in the file.
                add_game = False
        if add_game:
            # If the game wasn't flagged then add it.
            # Open the file and begin to edit it
            with open("data/game-log.json", "w") as game_file:
                # Create a var with the layout setup
                # Name, game name
                # Series, title of the comment,
                # Console, the console/'s its featured on
                # Details, description of the game
                # Link, this is generally the name but formated.
                # Other arrays for comments to be added
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
                    "page_creater": userID(current_user)["username"]
                }
                # Add the formated var to the gamelog.
                game_log.append(new_log)
                # Dump the data and new var and save them all into the file
                json.dump(game_log, game_file, indent=3)
                # Begin a function which will give the user
                # The same comment but in there account space
                # So that they can see it on there side.
                creditor(title, userID(
                    current_user)["username"], title, detail, "page")
        # Return the homepage once the games added
        return redirect({{url_for("index")}})


@app.route("/search", methods=["POST"])
def search():
    # This is the search page.
    # We take the form information and begin a function that uses that
    # data which is obtained from the form.
    text = request.form.get("Search")
    return result(text)


def error():
    # Return an error page and give the user understanding
    # that something has gone wrong with what they did.
    return render_template("error.html")


def result(query):
    #  Function to deal with users querys.
    # Start a file and results array
    file = []
    results = []
    # Check if the file exists.
    if not testFile("data/game-log.json"):
        # Return the error page if it doesnt exist.
        return error()
    # Open the game file as a var games_data
    with open("data/game-log.json", "r") as games_data:
        # Use file var and give it the game_data data
        # which has been converted using json load.
        file = json.load(games_data)
        # Start a for to compare the items in the file
        for i in range(len(file)):
            # If the query and the name of the game is equal continue
            if query.lower() in file[i]["name"].lower():
                # Add this game entry to the file array to export it
                # to the page.
                results.append(file[i])
        # Number of results which have been found to contain
        # the query the user has give them
        num = len(results)
        # If the amount of results is 0 return index.
        if num == 0 and "user_id" in session:
            return redirect({{url_for("index")}})
        # if the amount of results is 0 but user is active.
        elif num == 0 and "user_id" in session:
            # Return the inquire function to allow user to add page.
            return redirect({{url_for("inquire")}})
        else:
            # Render the results template with obtained information.
            return render_template(
                "result.html", results=(
                    results), num_search=(
                        num), query=(
                            query))


@app.route("/<game_name>", methods=["POST", "GET"])
def page_load(game_name):
    # Function to load the webpage with the game name.
    # When request method is POST
    if request.method == "POST":
        # If there is a current user continue
        if current_user is not None:
            # Get information from form and use it too write
            # the comment using involved data.
            user = userID(current_user)["username"]
            title = request.form.get("Title")
            tag = request.form.get("Radio")
            detail = request.form.get("Details")
            commentWrite(
                game_name, user, title, detail, tag)
    # Create an empty array
    file = []
    # Open the game file
    with open("data/game-log.json", "r") as games_data:
        # Open the file and load the file to var file with
        # json convertion.
        file = json.load(games_data)
        # Go though file and look though it.
        for obj in file:
            # Find the game that is currently in reference
            # using the link of the game provided.
            if obj["link"] == game_name:
                # Take the object using the link.
                # Use var game to hold the obj that is correct.
                game = obj
                # Begin to chaneg the var red and blue
                # to give the title a new colour
                # Check if the obj series and name are similar
                if obj["series"] in obj["name"]:
                    # Make the red the obj series
                    red = obj["series"]
                    # If the obj is different from the series and name
                    # then make them split and define a red and blue
                    # part to the title.
                    blue = obj["name"][len(obj["series"]):len(obj["name"])]
                else:
                    # Just make the title red if the series is not right.
                    red = obj["name"]
    # render the page template with the data thats obtained.
    # Find the current users ID
    if current_user is not None and userID(current_user) is not False:
        user = userID(current_user)["username"]
        return render_template(
            "page_template.html", game=game, red=red, blue=blue, user=user)
    else:
        return render_template(
            "page_template.html", game=game, red=red, blue=blue, user="")


def commentWrite(game_name, usern, title, comment, tag):
    # Function to write comments on the game-log file.
    with open("data/game-log.json", "r") as games:
        # Open the file and covert it using the json function.
        game_log = json.load(games)
        # Open the game log and look to find the game that matches.
        for i in range(len(game_log)):
            # Find the game that matches by the link.
            if game_name == game_log[i]["link"]:
                # Check if the comment isn't already added by mistake
                if comment not in game_log[i]["comment"]:
                    # Add the informaion that is required
                    game_log[i]["comment_title"].append(title)
                    game_log[i]["comment_tag"].append(tag)
                    game_log[i]["comment"].append(comment)
                    game_log[i]["author"].append(usern)
                    game_log[i]["num_comments"] = len(game_log[i]["comment"])
        # Open the file and edit it and add the information
        with open("data/game-log.json", "w") as file:
            # Once you add the new data and save it open a new
            # function
            json.dump(game_log, file, indent=3)
    # Within this function do the same as the previous function but
    # Add the comment to the users log so they can see what they have
    # added to the site.
    creditor(game_name, usern, title, comment, tag)


def userID(user_id):
    # Use the id to find the data about a user.
    # Use the id given to find the data required
    # by the different pages and functions.
    try:
        int(user_id)
        with open("data/users.json", "r") as users:
            # Open the users file and convert it using json.
            user_log = json.load(users)
            # Return the user using the id.
            return user_log[user_id-1]
    except Exception:
        return False


def creditor(game_name, usern, title, comment, tag):
    # This is the funtion to add a comment to the user
    # profile
    with open("data/users.json", "r") as users:
        # Open the file and convert it using the json load function.
        user_log = json.load(users)
        # Check though the user file for the users.
        for i in range(len(user_log)):
            # Once you find the user with the same name
            if usern == user_log[i]["username"]:
                # Check if the comment is new
                if comment not in user_log[i]["comment"]:
                    # Add the information to the users account
                    user_log[i]["game_title"].append(game_name)
                    user_log[i]["comment_title"].append(title)
                    user_log[i]["comment_tag"].append(tag)
                    user_log[i]["comment"].append(comment)
                    user_log[i]["num_comments"] = len(user_log[i]["comment"])
        # Open the file
        with open("data/users.json", "w") as file:
            # Add the data to the file and save/dump the file.
            json.dump(user_log, file, indent=3)


def testFile(file):
    # Function to try a file to check if it works or not.
    # If it exists then continue, else return an error.
    try:
        open(file, "r")
        return True
    except Exception:
        return False


if __name__ == "__main__":
    # Main function which sets up the app and .run variables/condit
    app.run(
        host=os.environ.get(
            "IP", "0.0.0.0"), port=int(
                os.environ.get(
                    "PORT", "5000")))
