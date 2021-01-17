from datetime import datetime, timedelta

import requests
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from flaskwebgui import FlaskUI  # get the FlaskUI class
import json
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config['SECRET_KEY'] = b'\xd4\xbd\x15\x84:U\xf5\xec\xf9\xcd"\x8d\xa6^lx'
ui = FlaskUI(app)  # feed the parameters


# do your logic as usual in Flask
def login_required(func):
    def secure_function(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for('index'))
        return func(*args, **kwargs)

    secure_function.__name__ = func.__name__

    return secure_function


def login(username, password):
    with open('players.json', 'r') as f:
        players = json.load(f)

    if username not in players:
        user = {'pwd': generate_password_hash(password),
                'wins': 0,
                'loses': 0,
                'ratio': 0.00}
        players[username] = user
        with open('players.json', 'w') as outfile:
            json.dump(players, outfile)

        session['username'] = username
        return True
    else:
        pwd = players[username]['pwd']
        connected = check_password_hash(pwd, password)

        if connected:
            session['username'] = username
            return True
        else:
            session.clear()
            return False


def randomize_page():
    r = requests.get("https://fr.wikipedia.org/w/api.php?format=json&action=query&generator=random&grnnamespace=0")
    pages = r.json()['query']['pages']

    title = pages[list(dict(pages).keys())[0]]['title']
    title = str.replace(title, " ", "_")
    return title


def get_page(title):
    url = f'https://fr.wikipedia.org/wiki/{title}'
    page = requests.get(url)

    soup = BeautifulSoup(page.text, features="lxml")

    page_py = soup.find('div', class_='mw-content-container')
    [o.decompose() for o in page_py.find_all(class_='mw-editsection')]
    [o.decompose() for o in page_py.find_all('sup', class_='reference')]

    for a in page_py.find_all('a', href=True):
        link_text = a['href']
        if ("/wiki/" in link_text and "wiktionary.org" not in link_text) or '#' in link_text:
            pass
        else:
            a.replaceWith(a.text)
    title = page_py.find('h1', class_='firstHeading').text

    return page_py, title


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form
        pseudo = data["inputPseudo"]
        pwd = data["inputPwd"]
        connected = login(pseudo, pwd)

        if connected:
            return redirect(url_for('lobby'))
        else:
            return redirect(url_for('index'))
    elif request.method == 'GET':
        if 'username' in session:
            return redirect(url_for('lobby'))
        else:
            return render_template('connection.html')


def verify_date(code_game):
    with open('games.json', 'r') as f:
        games = json.load(f)

    games[code_game]['maj'] = str(datetime.now())

    for code in games['codes']:
        if datetime.now() - datetime.fromisoformat(games[code_game]['maj']) > timedelta(minutes=2):
            delete_game(code)


@app.route('/wiki/<title>')
@login_required
def game(title):
    if request.referrer is None:
        return redirect(url_for('index'))

    session['n_clicks'] += 1

    if not request.script_root:
        request.script_root = url_for('index', _external=True)
    username = session['username']

    (page_py, title) = get_page(title)
    code_game = session['code_game']
    verify_date(code_game)
    nb_player = count_players(code_game)
    with open('games.json', 'r') as f:
        json_dict = json.load(f)
    game = json_dict[code_game]
    start_page = game['start_page']
    target_page = game['target_page']

    game[username] = session['n_clicks']

    json_dict[code_game] = game

    with open('games.json', 'w') as outfile:
        json.dump(json_dict, outfile)

    if title == target_page:
        finished(code_game, username)

    return render_template("main.html.twig", nombreJoueur=nb_player, code_game=code_game, page=page_py,
                           username=username, started_from=start_page, target=target_page, title=str.replace(title, " ", "_"), blocker=False, clics=session['n_clicks'])


def get_user(username):
    with open('players.json', 'r') as f:
        players = json.load(f)
    return players[username]


@app.route('/lobby', methods=['GET', 'POST'])
@login_required
def lobby():
    if 'username' in session:
        if not request.script_root:
            request.script_root = url_for('index', _external=True)
        username = session['username']
        delete_game(username)
        if request.method == 'POST':
            data = request.form
            if 'inputGame' in data:
                code_game = data['inputGame']
                # join game
                with open('games.json', 'r') as f:
                    json_dict = json.load(f)

                game = json_dict[code_game]
                start_page = game['start_page']
                target_page = game['target_page']
                session['n_clicks'] = 0

                game['players'].append(username)
                game['players'] = list(set(game['players']))
                game[username] = 0

                json_dict[code_game] = game

                with open('games.json', 'w') as outfile:
                    json.dump(json_dict, outfile)

                page_py = get_page(start_page)

                session['code_game'] = code_game
                return render_template("main.html.twig", code_game=code_game, page=page_py, username=username,
                                       started_from=start_page, target=target_page, blocker=True, clics=session['n_clicks'])
            else:
                # create game
                code_game = username
                start_page = randomize_page()
                target_page = randomize_page()
                with open(f'games.json', 'r') as f:
                    json_dict = json.load(f)

                json_dict['codes'].append(code_game)
                json_dict['codes'] = list(set(json_dict['codes']))
                json_dict[code_game] = {"host": username,
                                        "started": False,
                                        "players": [username],
                                        "winner": False,
                                        "start_page": start_page,
                                        "target_page": target_page,
                                        "maj": str(datetime.now()),
                                        username: 0
                                        }

                with open(f'games.json', 'w') as outfile:
                    json.dump(json_dict, outfile)

                session['start_page'] = start_page
                session['target_page'] = target_page
                session['code_game'] = code_game
                session['n_clicks'] = 0

                (page_py, title) = get_page(start_page)

                return render_template("main.html.twig", code_game=code_game, page=page_py, username=username,
                                       started_from=start_page, target=target_page, host=True, blocker=True, clics=session['n_clicks'])

        if request.method == 'GET':
            user = get_user(username)

            return render_template("lobby.html", username=username, user=user)
    else:
        return redirect(url_for('/'))


@app.route('/start', methods=['POST'])
@login_required
def start_game():
    data = request.form
    code_game = data['code_game']

    with open('games.json', 'r') as f:
        games = json.load(f)

    games[code_game]['started'] = True

    with open('games.json', 'w') as outfile:
        json.dump(games, outfile)

    return jsonify({"response": 200})


@app.route('/canIStart/<code_game>', methods=['GET'])
@login_required
def can_i_start(code_game):
    with open('games.json', 'r') as f:
        json_dict = json.load(f)
    game = json_dict[code_game]
    if game['started']:
        return jsonify({"response": 200})
    else:
        return jsonify({"response": 404})


@app.route('/<code_game>/numbersOfPlayer', methods=['GET'])
@login_required
def players(code_game):
    nb_players = count_players(code_game)
    return jsonify({"nombre": nb_players})


@app.route('/<code_game>/isFinished', methods=['GET'])
@login_required
def is_finished(code_game):
    with open('games.json', 'r') as f:
        games = json.load(f)

    players = games[code_game]["players"]
    classement = {}
    for player in players:
        classement[player] = games[code_game][player]

    if games[code_game]["winner"]:
        del classement[games[code_game]['winner']]

    return jsonify({"game": games[code_game], "classement": classement})


def finished(code_game, username):
    with open('games.json', 'r') as f:
        games = json.load(f)

    games[code_game]['winner'] = username

    with open('games.json', 'w') as outfile:
        json.dump(games, outfile)

    with open('players.json', 'r') as f:
        players = json.load(f)

    for p in games[code_game]["players"]:
        if username == p:
            players[p]["wins"] += 1
        else:
            players[p]["loses"] += 1
        players[p]["ratio"] = players[p]["wins"] / (players[p]["loses"]+players[p]["wins"])

    with open('players.json', 'w') as outfile:
        json.dump(players, outfile)

    return jsonify({"game": games[code_game]})


def count_players(code_game):
    with open('games.json', 'r') as f:
        games = json.load(f)
    nb_players = 0
    for player in games[code_game]['players']:
        nb_players += 1
    return nb_players


@app.route('/listGames', methods=['GET'])
def list_games():
    with open('games.json', 'r') as f:
        json_dict = json.load(f)
    games = []
    for game in json_dict['codes']:
        games.append(json_dict[game])
    games.reverse()
    return jsonify({"games": games})


def delete_game(code_game):
    with open('games.json', 'r') as f:
        json_dict = json.load(f)
    codes = json_dict['codes']
    try:
        codes.remove(code_game)
    except ValueError:
        pass
    json_dict['codes'] = codes

    try:
        del json_dict[code_game]
    except KeyError:
        pass

    with open('games.json', 'w') as outfile:
        json.dump(json_dict, outfile)


@app.route('/logout')
def logout():
    session.clear()

    return redirect("/")

#ui.run()
if __name__ == '__main__':
    app.run(host= '0.0.0.0')
