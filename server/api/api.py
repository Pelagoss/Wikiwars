from functools import wraps
from flask import Blueprint, jsonify, request, current_app, session
from flask_socketio import join_room

from .models import db, Game, User
from .tools import randomize_page, get_wiki_page, getSummaryWikiPage
from datetime import datetime, timedelta

import jwt

api = Blueprint('api', __name__)


def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()

        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]

            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user = User.query.filter_by(username=data['sub']).first()
            if not user:
                raise RuntimeError('User not found')
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401 # 401 is Unauthorized HTTP status code
        except jwt.InvalidTokenError as e:
            print(e)
            return jsonify(invalid_msg), 401

    return _verify


@api.route('/login', methods=('POST',))
def login():
    data = request.get_json()
    user = User.authenticate(**data)

    if not user:
        return jsonify({ 'message': 'Informations de connexion invalides', 'authenticated': False }), 401

    session['user'] = user.to_dict()

    token = jwt.encode({
        'sub': user.username,
        'iat':datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(days=1)},
        current_app.config['SECRET_KEY'])

    body = user.to_dict()
    body['jwt'] = token

    return jsonify(body)

@api.route('/game/create', methods=('POST',))
@token_required
def create_game(current_user):
    game = Game()
    game.users.append(current_user)
    game.host_id = current_user.id

    game.start = randomize_page()
    game.target = randomize_page()

    init_clics = dict()

    # Todo when start game
    init_clics[current_user.username] = {'clics': 0, 'page': game.start}

    game.clics = init_clics

    db.session.add(game)
    db.session.flush()
    db.session.commit()

    response = game.to_dict('game')
    return jsonify(response)

@api.route('/game/join', methods=('POST',))
@token_required
def join_game(current_user):
    game = Game.query.filter_by(id=request.get_json().get('id')).first()

    if current_user not in game.users:

        game.users.append(current_user)

        clics = game.clics

        clics[current_user.username] = {'clics': 0, 'page': game.start}

        game.clics = clics

        db.session.add(game)
        db.session.flush()
        db.session.commit()

    # socketio.emit("PLAYERS_CHANGED", len(game.users), broadcast=True, to=game.id)

    response = game.to_dict('game')
    return jsonify(response)


@api.route('/game/page/<path:title>', methods=('GET',))
@token_required
def get_page(current_user, title):
    try:
        game = Game.query.filter(Game.users.contains(current_user), Game.winner == None).first()

        # g.clics["Pelagoss"]["page"] = "France"
        game.clics[current_user.username] = {"clics": game.clics[current_user.username]["clics"] + 1, "page": title}
    except Exception as e:
        print(f'{e} ici')
        return jsonify({"message": str(e)}), 500
    print(request.args)
    if len(request.args):
        title = f'{title}?'
        if 'pagefrom' in request.args.keys():
            title += f'pagefrom={request.args["pagefrom"]}'
        if 'pageuntil' in request.args.keys():
            title += f'pageuntil={request.args["pageuntil"]}'

    page = get_wiki_page(title)

    room = f'{game.start}_{game.target}'

    event = "PAGE_CHANGED"

    if game.target == title.replace(' ', '_'):
        event = "GAME_FINISHED"
        game.winner_id = current_user.id

    db.session.commit()

    socketio().emit(event, game.to_dict('game'), broadcast=True, to = room)
    return page


@api.route('/game/link/<path:title>', methods=('GET',))
@token_required
def get_summary_page(current_user, title):
    return getSummaryWikiPage(title)

@api.route('/game/launch', methods=('POST',))
@token_required
def launch(current_user):
    try:
        game = Game.query.filter(Game.users.contains(current_user), Game.winner == None).first()

        print(current_user)
        print(game.host_id)
        if game.host_id == current_user.id:
            game.is_started = True

        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({"message": str(e)}), 500

    if game.is_started:
        room = f'{game.start}_{game.target}'
        socketio().emit("START_GAME", game.to_dict('game'), broadcast=True, to=room)
        return jsonify({'started': True})

    return jsonify({'started': False})


@api.route('/games', methods=('GET',))
@token_required
def getGames(current_user):
    response = [g.to_dict('game') for g in Game.query.all()]

    return jsonify(response)

def socketio():
    return current_app.extensions['socketio']