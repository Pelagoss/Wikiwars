import uuid

from flask import request, session
from flask.cli import FlaskGroup, with_appcontext
from flask_migrate import Migrate
from flask_socketio import join_room, leave_room
from sqlalchemy.sql.functions import current_user

from api.application import create_app, create_socket
from api.models import db, User, Game, u_g, mailer
from api.tools import send_mail

app = create_app()

migrate = Migrate()
migrate.init_app(app, db)

socketio = create_socket(app)

mailer.init_app(app)
cli = FlaskGroup(app)

@socketio.on('join')
def join(data):
    print("Joined room")
    session['room'] = f'{data["start"]}_{data["target"]}'
    join_room(session['room'])
    socketio.emit('ROOM_JOINED', to=current_user)


@socketio.on('leave')
def leave(data):
    leave_room(f'{data["start"]}_{data["target"]}')


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("email:register:comfirmation")
def re_send_confirmation():
    users = User.query.filter(User.validation_token != None).all()
    for u in users:
        u.validation_token = uuid.uuid4()

        db.session.add(u)
        db.session.flush()
        db.session.commit()
        send_mail('register', u, data={'pseudo': u.username, 'token': str(u.validation_token),
                                          'linkValider': f'[appUrl]/inscription/{u.validation_token}'})

# enable python shell with application context
@with_appcontext
def shell_ctx():
    return dict(app=app,
                db=db,
                User=User,
                Game=Game)

if __name__ == '__main__':
    cli()