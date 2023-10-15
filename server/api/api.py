from functools import wraps

from flask_socketio import SocketIO
import flask
from parse import *

import urllib.parse
from sqlalchemy import func, or_, and_
from sqlalchemy.sql import column, table
from flask import Blueprint, jsonify, request, current_app, session
from flask_socketio import join_room

from .models import db, Game, User, Email, Friendship, Avatar
from .tools import randomize_page, get_wiki_page, getSummaryWikiPage
from .tasks import notif_user_logged_in, send_mail, create_user
from datetime import datetime, timedelta

import jwt
import uuid

import redis
from rq import Queue, Connection

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

@api.route('/me', methods=('POST',))
@token_required
def me(current_user):
    return jsonify(current_user.to_dict())

@api.route('/login', methods=('POST',))
def login():
    data = request.get_json()
    (user, message) = User.authenticate(**data)

    if message:
        code = 401
        if user is not None:
            code = 403
            # user.validation_token = uuid.uuid4()
            #
            # db.session.add(user)
            # db.session.flush()
            # db.session.commit()
            # send_mail('register', user, data={'pseudo': user.username, 'token': str(user.validation_token),
            #                                   'linkValider': f'[appUrl]/inscription/{user.validation_token}'})
        return jsonify({ 'message': message, 'authenticated': False }), code

    session['user'] = user.to_dict()

    token = jwt.encode({
        'sub': user.username,
        'iat':datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(days=1)},
        current_app.config['SECRET_KEY'])

    # Say to everybody "I'm here"
    with Connection(redis.from_url(current_app.config["REDIS_URL"])):
        q = Queue()
        task = q.enqueue(notif_user_logged_in, args=(user,))

    body = user.to_dict()
    body['jwt'] = token

    resp = jsonify(body)

    resp.set_cookie('jwt_access_token', token)

    return resp

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
    with Connection(redis.from_url(current_app.config["REDIS_URL"])):
        q = Queue()
        task = q.enqueue(create_user, args=(current_app._get_current_object(), data,))

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

@api.route('/users', methods=('POST',))
@token_required
def get_user(current_user):
    data = request.get_json()

    f = User.query\
        .join(Friendship, and_(or_(User.id==Friendship.friend_id, User.id==Friendship.user_id), or_(Friendship.friend_id == current_user.id, Friendship.user_id == current_user.id)), isouter=True)\
        .with_entities(User.username, Friendship.status, Friendship.user_id, User.is_online, User.id, User.avatar)\
        .filter(User.username == data['username']).first()

    friend = User.query.filter(User.id == f[4]).first()
    stats = friend.to_dict()['stats']

    isInGame = len(list(filter(lambda g: g.winner_id is None, friend.games))) > 0 and f[1] == 'friends'
    joinableGame = list(filter(lambda g: g.winner_id is None and g.is_started == 0, friend.games))
    isJoinable = len(joinableGame) == 1 and f[1] == 'friends'

    response = {\
        'username': f[0],
        'relation': f[1],
        'user_id': f[2],
        'isOnline': f[3],
        'uid': f[4],
        'avatar': Avatar.query.filter_by(id = f[5]).first().to_dict(),
        'stats': stats,
        'isInGame': isInGame,
        'isJoinable': isJoinable\
    }

    if isJoinable is True:
        response['gameId'] = joinableGame[0].id

    return jsonify(response)

@api.route('/avatars', methods=('GET',))
@token_required
def get_list_avatars(current_user):
    f = Avatar.query\
        .join(table('user_avatar').join(User, and_(User.id==column('user_id'), User.id==current_user.id)), Avatar.id == column('avatar_id'), isouter=True)\
        .with_entities(Avatar.id, Avatar.path, column('avatar_id'))\
        .all()

    return jsonify([{'id': a[0], 'path': current_app.config['APP_URL_BACK'] + f'/static/avatar/{a[1]}', 'isUnlocked': a[2] is not None} for a in f])

@api.route('/avatars', methods=('POST',))
@token_required
def set_avatar(current_user):
    data = request.get_json()

    current_user.avatar = data['avatarId']

    db.session.flush()
    db.session.commit()
    return jsonify()

@api.route('/users-search', methods=('POST',))
@token_required
def search_user(current_user):
    data = request.get_json()

    users = User.query.filter(User.username != current_user.username, func.lower(User.username).like(f'%{data["username"].lower()}%'))

    users = users.all()

    return jsonify([u.to_dict() for u in users])

@api.route('/friends', methods=('GET',))
@token_required
def get_friends(current_user):
    friends_list = User.query\
        .join(Friendship, or_(User.id==Friendship.friend_id, User.id==Friendship.user_id))\
        .with_entities(User.username, Friendship.status, Friendship.user_id, User.is_online, User.avatar)\
        .filter(User.id != current_user.id, or_(Friendship.user_id==current_user.id, Friendship.friend_id==current_user.id))\
        .order_by(Friendship.created_at)\
        .all()

    return jsonify([{'username': f[0], 'status': f[1], 'user_id': f[2], 'isOnline': f[3], 'avatar': Avatar.query.filter_by(id = f[4]).first().to_dict()} for f in friends_list])

@api.route('/friends/add', methods=('POST',))
@token_required
def add_friends(current_user):
    data = request.get_json()
    friend_invitation = Friendship()
    friend_invitation.user_id = current_user.id
    friend_invitation.friend_id = data['friend_id']
    friend_invitation.status = 'pending'

    db.session.add(friend_invitation)
    db.session.flush()
    db.session.commit()

    sid = User.query.filter_by(id=data['friend_id']).first().sid
    if sid is not None:
        socketio().emit('NEW_FRIEND_INVITATION', current_user.username, to=sid)

    return jsonify()


@api.route('/friends', methods=('POST',))
@token_required
def handle_friends_invitation(current_user):
    data = request.get_json()
    friend_invitation = Friendship.query.filter_by(user_id = data['user_id'], friend_id = current_user.id, status = 'pending').first()

    if data['accept'] is True:
        friend_invitation.status = 'friends'
        sid = User.query.filter_by(id=data['user_id']).first().sid
        if sid is not None:
            socketio().emit('NEW_FRIEND', current_user.username, to=sid)
            db.session.add(friend_invitation)
    else:
        friend_invitation.status = 'refused'
        db.session.delete(friend_invitation)

    db.session.flush()
    db.session.commit()

    friends_list = User.query\
            .join(Friendship, or_(User.id==Friendship.friend_id, User.id==Friendship.user_id))\
            .with_entities(User.username, Friendship.status, Friendship.user_id, User.is_online)\
            .filter(User.id != current_user.id, or_(Friendship.user_id==current_user.id, Friendship.friend_id==current_user.id))\
            .order_by(Friendship.created_at)\
            .all()

    return jsonify([{'username': f[0], 'status': f[1], 'user_id': f[2], 'isOnline': f[3]} for f in friends_list])


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