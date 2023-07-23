from functools import wraps

import flask
from parse import *

import urllib.parse
from sqlalchemy import func
from flask import Blueprint, jsonify, request, current_app, session
from flask_socketio import join_room

from .models import db, Game, User, Email
from .tools import randomize_page, get_wiki_page, getSummaryWikiPage, send_mail
from datetime import datetime, timedelta

import jwt
import uuid

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



@api.route('/')
def index():
    return flask.render_template('index.html')

@api.route('/login', methods=('POST',))
def login():
    data = request.get_json()
    (user, message) = User.authenticate(**data)

    if message:
        code = 401
        if user is not None:
            code = 403
            user.validation_token = uuid.uuid4()

            db.session.add(user)
            db.session.flush()
            db.session.commit()
            send_mail('register', user, data={'pseudo': user.username, 'token': str(user.validation_token),
                                              'linkValider': f'[appUrl]/inscription/{user.validation_token}'})
        return jsonify({ 'message': message, 'authenticated': False }), code

    session['user'] = user.to_dict()

    token = jwt.encode({
        'sub': user.username,
        'iat':datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(days=1)},
        current_app.config['SECRET_KEY'])

    body = user.to_dict()
    body['jwt'] = token

    return jsonify(body)

@api.route('/register', methods=('POST',))
def register():
    data = request.get_json()

    (is_valid, error, field) = User.verify_form('register', **data)
    if not is_valid:
        return jsonify({ 'message': error, 'fields': [field], 'authenticated': False }), 401

    fields = []

    if User.query.filter(func.lower(User.username) == func.lower(data.get('username'))).first() is not None:
        fields.append('username')
    if User.query.filter(func.lower(User.email) == func.lower(data.get('email'))).first() is not None:
        fields.append('email')
    if len(fields) > 0:
        return jsonify({ 'message': f'Votre [field] : [field_value] existe déjà', 'fields': fields, 'authenticated': False }), 403

    #Create account, send email and generate a validation token
    user = User(email = data.get('email').lower(), username = data.get('username'), password = data.get('password'))
    user.validation_token = uuid.uuid4()

    db.session.add(user)
    db.session.flush()
    db.session.commit()

    msg = send_mail('register', user, data={'pseudo': user.username, 'token': str(user.validation_token), 'linkValider': f'[appUrl]/inscription/{user.validation_token}'})

    return jsonify(True)

@api.route('/register/confirm/<uuid:token>', methods=('POST',))
def confirmation(token):
    user = User.query.filter_by(validation_token=token).first()

    try:
        user.validation_token = None

        db.session.add(user)
        db.session.flush()
        db.session.commit()
    except Exception as e:
        return jsonify({ 'message': f'Compte non validé', 'authenticated': False }), 403

    return jsonify(True)

@api.route('/email/download/<uuid:unique_token>', methods=('POST',))
def download_email(unique_token):
    email = Email.query.filter_by(unique_token=unique_token).first()

    return jsonify(email.message_html)

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

    socketio().emit("NEW_GAME", game.to_dict('game'), to='lobby')

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

    response = game.to_dict('game')
    return jsonify(response)


@api.route('/game/page/<path:title>', methods=('GET',))
@token_required
def get_page(current_user, title):
    try:
        game = Game.query.filter(Game.users.contains(current_user), Game.winner == None).first()

        game.clics[current_user.username] = {"clics": game.clics[current_user.username]["clics"] + 1, "page": title}
    except Exception as e:
        return jsonify({"message": str(e)}), 500

    if len(request.args):
        title = f'{title}?'
        if 'pagefrom' in request.args.keys():
            title += f'pagefrom={request.args["pagefrom"]}'
        if 'pageuntil' in request.args.keys():
            title += f'pageuntil={request.args["pageuntil"]}'

    page = get_wiki_page(title)

    room = f'{game.start}_{game.target}'

    event = "PAGE_CHANGED"

    if game.target == urllib.parse.unquote(title).replace(' ', '_'):
        event = "GAME_FINISHED"
        game.winner_id = current_user.id
        socketio().emit("FINISH_GAME", game, to='lobby')

    db.session.commit()

    socketio().emit(event, game.to_dict('game'), to = room)
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

        if game.host_id == current_user.id:
            game.is_started = True
            game.started_at = datetime.utcnow()

        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({"message": str(e)}), 500

    if game.is_started:
        room = f'{game.start}_{game.target}'
        socketio().emit("START_GAME", game.to_dict('game'), to=room)
        socketio().emit("GAME_STARTED", game.to_dict('game'), to='lobby')

        return jsonify({'started': True})

    return jsonify({'started': False})


@api.route('/games', methods=('GET',))
@token_required
def getGames(current_user):
    response = [g.to_dict('game') for g in Game.query.all()]

    return jsonify(response)

def socketio():
    return current_app.extensions['socketio']