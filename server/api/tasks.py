from .models import db, Game, User, Email, Friendship, Avatar

from flask import render_template
from .application import create_app
from flask_socketio import SocketIO
from .tools import send_mail

app = create_app()

socketio = SocketIO(message_queue=app.config["REDIS_URL"])

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import insert, table, column, select, update

users_avatars = table('user_avatar',
        column('avatar_id'),
        column('user_id')
    )

def create_user(app, data):
    user = User(email = data.get('email').lower(), username = data.get('username'), password = data.get('password'))
    user.validation_token = uuid.uuid4()

    db.session.add(user)
    db.session.flush()
    db.session.commit()

    with app.app_context():
        send_mail('register', user, data={'pseudo': user.username, 'token': str(user.validation_token), 'linkValider': f'[appUrl]/inscription/{user.validation_token}'})

    bind = op.get_bind()
    session = sa.orm.Session(bind=bind)

    idAvatars = Avatar.query\
            .with_entities(Avatar.id)\
            .filter(Avatar.condition_type == 'free').all()

    for idA in idAvatars:
        dataAvatar = {
            "avatar_id": idA[0],
            "user_id": u[0]
        }

        session.execute(insert(users_avatars).values(dataAvatar))

def notif_user_logged_in(user):
    friends_list = User.query\
            .join(Friendship, or_(User.id==Friendship.friend_id, User.id==Friendship.user_id))\
            .with_entities(User.sid)\
            .filter(User.id != user.id, or_(Friendship.user_id==user.id, Friendship.friend_id==user.id), Friendship.status == 'friends', User.is_online == True)\
            .order_by(Friendship.created_at)\
            .all()

    socketio.emit('FRIEND_ONLINE', user.username, to=[f[0] for f in friends_list])