from flask import request, session
from flask.cli import FlaskGroup, with_appcontext
from flask_mailalchemy.core import MailAlchemy
from flask_migrate import Migrate
from flask_socketio import join_room, leave_room
from sqlalchemy.sql.functions import current_user

from api.application import create_app, create_socket
from api.models import db, User, Game, u_g, mailer

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


# enable python shell with application context
@with_appcontext
def shell_ctx():
    return dict(app=app,
                db=db,
                User=User,
                Game=Game)

if __name__ == '__main__':
    cli()