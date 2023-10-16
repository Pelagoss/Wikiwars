from .models import Game, User, Email, Friendship, Avatar

from sqlalchemy import func, or_, and_

from .application import create_app, db
from flask_socketio import SocketIO
from .tools import send_mail
import uuid
import time

app = create_app()
app.app_context().push()

socketio = SocketIO(message_queue=app.config["REDIS_URL"])

from sqlalchemy.sql import insert, table, column, select, update

users_avatars = table('user_avatar',
        column('avatar_id'),
        column('user_id')
    )

def create_user(email):
    user = User.query.filter_by(email=email).first()

    send_mail('register', user, {'pseudo': user.username, 'token': str(user.validation_token), 'linkValider': f'[appUrl]/inscription/{user.validation_token}'}, True)

    idAvatars = Avatar.query\
                .with_entities(Avatar.id)\
                .filter(Avatar.condition_type == 'free').all()

    for idA in idAvatars:
        dataAvatar = {
            "avatar_id": idA[0],
            "user_id": user.id
        }

        db.session.execute(insert(users_avatars).values(dataAvatar))
    db.session.flush()
    db.session.commit()

def notif_user_logged_in(user):
    friends_list = User.query\
            .join(Friendship, or_(User.id==Friendship.friend_id, User.id==Friendship.user_id))\
            .with_entities(User.sid)\
            .filter(User.id != user.id, or_(Friendship.user_id==user.id, Friendship.friend_id==user.id), Friendship.status == 'friends', User.is_online == True)\
            .order_by(Friendship.created_at)\
            .all()

    socketio.emit('FRIEND_ONLINE', user.username, to=[f[0] for f in friends_list])