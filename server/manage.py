import uuid

from flask import request, session
from flask.cli import FlaskGroup, with_appcontext
from flask_socketio import join_room, leave_room
from sqlalchemy.sql.functions import current_user

from api.application import create_app
from api.models import db, User, Game, u_g
from api.tools import send_mail

import redis
from rq import Connection, Worker

app = create_app()

cli = FlaskGroup(app)

socketio = app.extensions['socketio']

@socketio.on('join')
def join(data):
    if isinstance(data, str):
        session['room'] = 'lobby'
    else:
        session['room'] = f'{data["start"]}_{data["target"]}'
    print(f'Room : {session["room"]} joined !')
    join_room(session['room'])
    socketio.emit('ROOM_JOINED', to=current_user)


@socketio.on('connect')
def connect(auth):
    u = User.query.filter(User.id == auth['id']).first()
    session['user'] = u
    u.is_online = True
    u.sid = request.sid
    db.session.add(u)
    db.session.flush()
    db.session.commit()


@socketio.on('disconnect')
def disconnect():
    u = session['user']
    u.is_online = False
    db.session.add(u)
    db.session.flush()
    db.session.commit()

    session['user'] = None

@socketio.on('leave')
def leave(data):
    leave_room(f'{data["start"]}_{data["target"]}')


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("email:register:confirmation")
def re_send_confirmation():
    users = User.query.filter(User.validation_token != None).all()
    for u in users:
        u.validation_token = uuid.uuid4()

        db.session.add(u)
        db.session.flush()
        db.session.commit()

        with Connection(redis.from_url(app.config["REDIS_URL"])):
            q = Queue()
            task = q.enqueue(send_mail, args=('registerRelance', u, {'pseudo': u.username, 'token': str(u.validation_token),
                                                                                        'linkValider': f'[appUrl]/inscription/{u.validation_token}'},))

@cli.command("run_worker")
def run_worker():
    redis_url = app.config["REDIS_URL"]
    redis_connection = redis.from_url(redis_url)
    with Connection(redis_connection):
        worker = Worker(app.config["QUEUES"])
        worker.work()

# enable python shell with application context
@with_appcontext
def shell_ctx():
    return dict(app=app,
                db=db,
                User=User,
                Game=Game)

if __name__ == '__main__':
    cli()