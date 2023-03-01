from functools import wraps
from flask import Blueprint, jsonify, request, current_app
from .models import db, Game, User
from .tools import randomize_page
from datetime import datetime, timedelta
import pickle

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
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401

    return _verify


@api.route('/login/', methods=('POST',))
def login():
    data = request.get_json()
    user = User.authenticate(**data)

    if not user:
        return jsonify({ 'message': 'Informations de connexion invalides', 'authenticated': False }), 401

    token = jwt.encode({
        'sub': user.username,
        'iat':datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=30)},
        current_app.config['SECRET_KEY'])

    return jsonify({ 'token': token })

@api.route('/game/create', methods=('POST',))
@token_required
def create_game(current_user):
    game = Game()
    game.users.append(current_user)

    game.start = randomize_page()
    game.target = randomize_page()

    init_clics = dict()

    # Todo when start game
    # for p in game.users:
    #     init_clics[p.username] = {'clics': 0, 'page': game.start}

    game.clics = pickle.loads(pickle.dumps(init_clics))

    db.session.add(game)
    db.session.flush()
    db.session.commit()

    response = game.to_dict('game')
    return jsonify(response)