from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

u_g = db.Table('user_game',
    db.Column('game_id', db.Integer, db.ForeignKey('games.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    games = db.relationship('Game', secondary=u_g, lazy='subquery', backref=db.backref('users', lazy=True))

    def to_dict(self):
        return dict(id=self.id,
                    username=self.username,
                    created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    games=[game.to_dict() for game in self.games])

class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.String(500), nullable=False)
    target = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    winner = db.Column(db.String(500), nullable=True)
    clics = db.Column(db.PickleType)

    def to_dict(self):
        return dict(id=self.id,
                    start=self.start,
                    target=self.target,
                    created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    winner=self.winner.to_dict(),
                    clics=self.clics)