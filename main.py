import requests
from flask import Flask, render_template, request, redirect, url_for, session
from flaskwebgui import FlaskUI   # get the FlaskUI class
import wikipedia
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = b'\xd4\xbd\x15\x84:U\xf5\xec\xf9\xcd"\x8d\xa6^lx'
ui = FlaskUI(app)                 # feed the parameters


# do your logic as usual in Flask
def randomize_page():
    r = requests.get("https://fr.wikipedia.org/w/api.php?format=json&action=query&generator=random&grnnamespace=0")
    pages = r.json()['query']['pages']

    title = pages[list(dict(pages).keys())[0]]['title']
    return title


@app.route("/", methods=['GET', 'POST'])
def index():
    with open('players.json', 'r') as f:
        json_dict = json.load(f)

    players = json_dict['players']
    if request.method == 'POST':
        data = request.form
        pseudo = data["inputPseudo"]

        if pseudo not in players:
            json_dict['players'].append(pseudo)
            with open('players.json', 'w') as outfile:
                json.dump(json_dict, outfile)

            session['username'] = pseudo

            return redirect(url_for('index'))
        if pseudo in players and 'username' in session and session['username'] == pseudo:
            return redirect(url_for('index'))
        else:
            return render_template("connection.html", error="Pseudo déjà utilisé !")
    if request.method == 'GET':
        if 'username' in session and session['username'] in players:
            return f'Connecté {session["username"]}'
        else:
            return render_template("connection.html")

@app.route("/wiki/<title>")
def next(title):
    username = session['username']
    wikipedia.set_lang("fr")
    page_py = wikipedia.page(title, auto_suggest=True).html()
    return render_template("main.html", page=page_py, username=username, started_from="depart", target="Hitler")

ui.run()