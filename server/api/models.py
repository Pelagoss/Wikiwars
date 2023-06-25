import re
from abc import ABC
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.mutable import MutableDict
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import MetaData
from .tools import to_dict

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


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


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    games = db.relationship('Game', secondary=u_g, lazy='subquery', backref=db.backref('users', lazy=True))
    wins = db.relationship('Game', backref="winner", lazy=False)

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

    @classmethod
    def authenticate(cls, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')

        if not username or not password:
            return None

        user = cls.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return None

        return user

    @classmethod
    def verify_form(cls, formType, **kwargs):
        form_fields = []
        if formType is 'register':
            form_fields = ['email', 'username', 'password', 'passwordConfirm']

        for field in form_fields:
            if cls.validate_field(kwargs.get(field), field) is not True:
                return False

        return True

    @classmethod
    def validate_field(cls, field_value, field_type):
        errors = []
        is_valid = True

        if field_value is None:
            return False, "La valeur ne peut pas être vide"

        if field_type is 'email':
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

            if not re.fullmatch(regex, field_value):
                is_valid = False
                errors = 'Votre email est invalide'

            return is_valid, errors
        elif field_type is 'password' or field_type is 'passwordConfirm':
            if not any(x.isupper() for x in field_type):
                errors.append('contenir au moins 1 majuscule')
            if not any(x.islower() for x in field_type):
                errors.append('contenir au moins 1 minuscule')
            if not any(x.isdigit() for x in field_type):
                errors.append('contenir au moins 1 chiffre')
            if not len(field_type) >= 7:
                errors.append('contenir au moins 7 caractères')

            if len(errors) > 0:
                is_valid = False
                errors = "Votre mot de passe doit" + ", ".join(errors) + "."

            return is_valid, errors

        elif field_type is 'username':
            if not len(field_type) >= 7:
                errors.append('contenir au moins 7 caractères')

            if len(errors) > 0:
                is_valid = False
                errors = "Votre nom doit" + ", ".join(errors) + "."

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
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
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
            d['started_at'] = datetime.timestamp(self.started_at)

        if type == 'game':
            d['users'] = [u.to_dict(type) for u in self.users]
            if self.winner_id is not None:
                d['winner'] = User.query.filter_by(id=self.winner_id).first().to_dict(type)
            return d
        else:
            return d
