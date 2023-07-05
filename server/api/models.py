import re
from abc import ABC
from datetime import datetime

from flask_mail import Mail, Message
from flask_sqlalchemy.extension import SQLAlchemy
from sqlalchemy.ext.mutable import MutableDict
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import MetaData, Uuid, String, UniqueConstraint

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)
mailer = Mail()

from sqlalchemy.types import TypeDecorator, VARCHAR
import json

class JSONEncodedDict(TypeDecorator, ABC):
    "Represents an immutable structure as a json-encoded string."

    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


u_g = db.Table('user_game',
               db.Column('game_id', db.Integer, db.ForeignKey('games.id'), primary_key=True),
               db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
               )

class Email(db.Model):
    __tablename__ = 'emails'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    sender_address = db.Column(db.String(255), nullable=False, index=True)
    sender_name = db.Column(db.String(80))
    subject = db.Column(db.String(80), nullable=False, index=True)
    recipient = db.Column(db.String(255), nullable=False, index=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    type = db.Column(String)
    unique_token = db.Column(db.Uuid)
    message_txt = db.Column(db.Text)
    message_html = db.Column(db.Text)

    sent_at = db.Column(
        db.DateTime,
        index=True
    )
    error = db.Column(db.Text)

    @property
    def message(self) -> Message:
        sender = self.sender_address \
            if self.sender_name is None \
            else (self.sender_name, self.sender_address)
        msg = Message(
            self.subject,
            [self.recipient],
            self.message_txt,
            self.message_html,
            sender
        )

        return msg

    @classmethod
    def from_message(cls, msg: Message) -> tuple:
        messages = []
        if isinstance(msg.recipients, str):
            recipients = [msg.recipients]
        else:
            recipients = msg.recipients

        if msg.sender.endswith(">"):
            separator = msg.sender.rfind("<")
            sender_address = msg.sender[separator + 1:-1]
            sender_name = msg.sender[:separator].strip()
        else:
            sender_address = msg.sender
            sender_name = None

        subject = msg.subject
        message_html = msg.html
        message_txt = msg.body

        for recipient in recipients:
            email = cls()
            email.recipient = recipient
            if isinstance(recipient, User):
                email.recipient_id = recipient.id
            email.recipient = recipient
            email.sender_address = sender_address
            email.sender_name = sender_name
            email.subject = subject
            email.message_html = message_html
            email.message_txt = message_txt

            messages.append(email)

        return tuple(messages)


class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = (
        UniqueConstraint('email', name='uix_user_email'),
        UniqueConstraint('username', name='uix_user_username'),
    )

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(String)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    validation_token = db.Column(db.Uuid)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    games = db.relationship('Game', secondary=u_g, lazy='subquery', backref=db.backref('users', lazy=True))
    wins = db.relationship('Game', backref="winner", lazy=False)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = generate_password_hash(password)

    @classmethod
    def authenticate(cls, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')

        if not username or not password:
            return None, 'Informations de connexion invalides'

        user = cls.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return None, 'Informations de connexion invalides'
        if user.validation_token is not None:
            return user, 'Adresse email non validée, vérifiez vos emails'

        return user, None

    @classmethod
    def verify_form(cls, formType, **kwargs):
        form_fields = []
        if formType == 'register':
            form_fields = ['email', 'username', 'password', 'passwordConfirm']

        for field in form_fields:
            (is_valid, error) = cls.validate_field(kwargs.get(field), field)
            if is_valid is False:
                return is_valid, error, field

        return True, None, None

    @classmethod
    def validate_field(cls, field_value, field_type):
        errors = []
        is_valid = True

        if field_value is None:
            return False, f'La valeur du champ [{field_type}] ne peut pas être vide'

        if field_type == 'email':
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

            if not re.fullmatch(regex, field_value):
                is_valid = False
                errors = f'Votre [{field_type}] est invalide'

            return is_valid, errors

        elif field_type == 'password' or field_type == 'passwordConfirm':
            if not any(x.isupper() for x in field_value):
                errors.append('1 majuscule')
            if not any(x.islower() for x in field_value):
                errors.append('1 minuscule')
            if not any(x.isdigit() for x in field_value):
                errors.append('1 chiffre')
            if not len(field_value) >= 7:
                errors.append('7 caractères')

            if len(errors) > 0:
                is_valid = False
                errors = f'Votre [{field_type}] doit contenir au moins {", ".join(errors)}.'

            return is_valid, errors

        elif field_type == 'username':
            if not len(field_value) >= 7:
                errors.append('contenir au moins 7 caractères')

            if len(errors) > 0:
                is_valid = False
                errors = f'Votre [{field_type}] doit {", ".join(errors)}.'

            return is_valid, errors

    def to_dict(self, type = None):
        d = dict(id=self.id, username=self.username)

        if type == 'game':
            return d
        else:
            d['games'] = [game.to_dict() for game in self.games]
            d['wins'] = [win.to_dict() for win in self.wins]
            return d


class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    is_started = db.Column(db.Boolean, default=False)
    start = db.Column(db.String(500), nullable=False)
    target = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    started_at = db.Column(db.DateTime)
    winner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    host_id = db.Column(db.Integer, nullable=False)
    clics = db.Column(MutableDict.as_mutable(JSONEncodedDict))

    def to_dict(self, type = None):
        d = dict(id=self.id,
                 is_started=self.is_started,
                 start=self.start,
                 target=self.target,
                 winner=self.winner_id,
                 host=self.host_id,
                 clics=self.clics)

        if self.started_at is not None:
            d['started_at'] = datetime.isoformat(self.started_at)

        if type == 'game':
            d['users'] = [u.to_dict(type) for u in self.users]
            if self.winner_id is not None:
                d['winner'] = User.query.filter_by(id=self.winner_id).first().to_dict(type)
            return d
        else:
            return d
