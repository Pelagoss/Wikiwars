from .models import db, Game, User, Email, Friendship, Avatar

from flask import render_template
from .application import create_app
from flask_socketio import SocketIO
from flask_mail import Mail

from .config import BaseConfig

config = BaseConfig.__dict__

mailer = Mail()
socketio = SocketIO(message_queue=config["REDIS_URL"])

def send_mail(type_mail, user, data):
    if isinstance(user, str):
        recipients = [user]
    else:
        recipients = [user.email]

    appUrl = config['APP_URL']
    appUrlBack = config['APP_URL_BACK']

    data['appUrl'] = appUrl
    data['appUrlBack'] = appUrlBack

    for key, value in data.items():
        data[key] = value.replace('[appUrl]', appUrl)

    if type_mail == 'register':
        subject = 'Confirmez votre inscription !'
    elif type_mail == 'registerRelance':
        subject = '[Relance] Confirmez votre inscription !'
    else:
        subject = 'Consultez les WikiNews !'

    msg = Message(
        subject=subject,
        sender=(config['MAIL_SENDER'], config['MAIL_ADDRESS']),
        recipients=recipients
    )

    unique_token = uuid.uuid4()

    data['browserLink'] = f'{appUrl}/emails/{unique_token}'

    msg.html = render_template(
            "mail/{}.html".format(type_mail),
            **data
        )

    emails = Email.from_message(msg)
    for email in emails:
        email.unique_token = unique_token
        email.type = type_mail
        email.recipient_id = user.id

        db.session.add(email)
        db.session.flush()
        db.session.commit()

    mailer.send(msg)

    return None

def notif_user_logged_in(user):
    friends_list = User.query\
            .join(Friendship, or_(User.id==Friendship.friend_id, User.id==Friendship.user_id))\
            .with_entities(User.sid)\
            .filter(User.id != user.id, or_(Friendship.user_id==user.id, Friendship.friend_id==user.id), Friendship.status == 'friends', User.is_online == True)\
            .order_by(Friendship.created_at)\
            .all()

    socketio.emit('FRIEND_ONLINE', user.username, to=[f[0] for f in friends_list])