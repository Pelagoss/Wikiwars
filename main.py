import requests
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

from flaskwebgui import FlaskUI  # get the FlaskUI class
import json
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config['SECRET_KEY'] = b'\xd4\xbd\x15\x84:U\xf5\xec\xf9\xcd"\x8d\xa6^lx'
ui = FlaskUI(app)  # feed the parameters


# do your logic as usual in Flask
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
        if "/wiki/" not in link_text or "wiktionary" in link_text:
            a.replaceWith(a.text)

    return page_py

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
    elif request.method == 'GET':
        if 'username' in session:
            return redirect(url_for('lobby'))
        else:
            return render_template("connection.html")


@app.route('/wiki/<title>')
def game(title):
    if request.referrer is None:
        return redirect(url_for('index'))

    session['n_clicks'] += 1

    if not request.script_root:
        request.script_root = url_for('index', _external=True)
    username = session['username']

    page_py = get_page(title)
    code_game = session['code_game']
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

    return render_template("main.html.twig", nombreJoueur=nb_player, code_game=code_game, page=page_py,
                           username=username, started_from=start_page, target=target_page, title=str.replace(title, " ", "_"), blocker=False, clics=session['n_clicks'])


@app.route('/lobby', methods=['GET', 'POST'])
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
                                        username: 0
                                        }

                with open(f'games.json', 'w') as outfile:
                    json.dump(json_dict, outfile)

                session['start_page'] = start_page
                session['target_page'] = target_page
                session['code_game'] = code_game
                session['n_clicks'] = 0

                page_py = get_page(start_page)

                return render_template("main.html.twig", code_game=code_game, page=page_py, username=username,
                                       started_from=start_page, target=target_page, host=True, blocker=True, clics=session['n_clicks'])

        if request.method == 'GET':
            return render_template("lobby.html", username=username)
    else:
        return redirect(url_for('/'))


@app.route('/start', methods=['POST'])
def start_game():
    data = request.form
    code_game = data['code_game']

    with open('games.json', 'r') as f:
        json_dict = json.load(f)
    game = json_dict[code_game]
    game['started'] = True
    json_dict[code_game] = game
    with open('games.json', 'w') as outfile:
        json.dump(json_dict, outfile)

    return jsonify({"response": 200})


@app.route('/canIStart/<code_game>', methods=['GET'])
def can_i_start(code_game):
    with open('games.json', 'r') as f:
        json_dict = json.load(f)
    game = json_dict[code_game]
    if game['started']:
        return jsonify({"response": 200})
    else:
        return jsonify({"response": 404})


@app.route('/<code_game>/numbersOfPlayer', methods=['GET'])
def players(code_game):
    nb_players = count_players(code_game)
    return jsonify({"nombre": nb_players})


@app.route('/<code_game>/isFinished', methods=['GET'])
def is_finished(code_game):
    with open('games.json', 'r') as f:
        json_dict = json.load(f)

    game = json_dict[code_game]


    return jsonify({"game": game})


@app.route('/<code_game>/finished', methods=['POST'])
def finished(code_game):
    data = request.form
    user = data['username']

    with open('games.json', 'r') as f:
        json_dict = json.load(f)

    game = json_dict[code_game]

    game['winner'] = user

    json_dict[code_game] = game

    with open('games.json', 'w') as outfile:
        json.dump(json_dict, outfile)

    return jsonify({"game": game})


def count_players(code_game):
    with open('games.json', 'r') as f:
        json_dict = json.load(f)
    game = json_dict[code_game]
    nb_players = 0
    for player in game['players']:
        nb_players += 1
    return nb_players


@app.route('/listGames', methods=['GET'])
def list_games():
    with open('games.json', 'r') as f:
        json_dict = json.load(f)
    games = []
    for game in json_dict['codes']:
        games.append(json_dict[game])
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

    with open('players.json', 'r') as f:
        json_dict = json.load(f)

    players = json_dict['players']
    players.remove(session['username'])
    json_dict['players'] = players

    with open(f'players.json', 'w') as outfile:
        json.dump(json_dict, outfile)

    session.clear()

    return redirect("/")

#ui.run()
app.run(host= '0.0.0.0')
