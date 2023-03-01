from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
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

    def to_dict(self, type = None):
        d = dict(username=self.username)

        if type == 'game':
            return d
        else:
            d['games'] = [game.to_dict() for game in self.games]
            return d


class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    is_started = db.Column(db.Boolean, default=False)
    start = db.Column(db.String(500), nullable=False)
    target = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    winner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    clics = db.Column(db.PickleType)

    def to_dict(self, type = None):
        d = dict(id=self.id,
                 is_started=self.is_started,
                 start=self.start,
                 target=self.target,
                 winner=to_dict(self.winner_id),
                 clics=self.clics)

        if type == 'game':
            d['users'] = [u.to_dict(type) for u in self.users]
            return d
        else:
            return d
