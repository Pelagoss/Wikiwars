from flask import Flask, render_template, request
from flaskwebgui import FlaskUI   # get the FlaskUI class
import wikipedia
import json


app = Flask(__name__)
ui = FlaskUI(app)                 # feed the parameters


# do your logic as usual in Flask

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ip_address = request.remote_addr
        data = request.form
        print(data)
        pseudo = data["inputPseudo"]

        with open('players.json', 'r') as f:
            json_dict = json.load(f)

        players = json_dict

        print(players)

        if ip_address not in players:
            players[ip_address] = pseudo
            with open('players.json', 'w') as outfile:
                json.dump(players, outfile)

            wikipedia.set_lang("fr")
            page_py = wikipedia.page("Germany").html()
            return render_template("main.html", page=page_py, username=pseudo, started_from="depart", target="Hitler")
        else:
            return render_template("connection.html", error="")
    if request.method == 'GET':
        return render_template("connection.html", error="")


@app.route("/wiki/<title>")
def next(title):
    ip_address = request.remote_addr
    with open('players.json', 'r') as f:
        json_dict = json.load(f)
    players = json_dict
    username = players[ip_address]
    wikipedia.set_lang("fr")
    page_py = wikipedia.page(title, auto_suggest=True).html()
    return render_template("main.html", page=page_py, username=username, started_from="depart", target="Hitler")

ui.run()