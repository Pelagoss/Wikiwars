from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

def create_app(app_name='WIKI_API'):
    app = Flask(app_name)
    app.config.from_object('api.config.BaseConfig')
    from api.api import api
    app.register_blueprint(api, url_prefix="/api")
    CORS(app)

    from api.models import db
    db.init_app(app)

    return app

def create_socket(app):
    return SocketIO(app, cors_allowed_origins="*")