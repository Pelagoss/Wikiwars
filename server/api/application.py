from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_migrate import Migrate
from sqlalchemy import MetaData
from flask_sqlalchemy.extension import SQLAlchemy

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)

def create_app(app_name='WIKI_API'):
    app = Flask(app_name)
    app.config.from_object('api.config.BaseConfig')
    from api.api import api
    app.register_blueprint(api, url_prefix="/api")

    db.init_app(app)

    CORS(app, supports_credentials=True)

    migrate = Migrate()
    migrate.init_app(app, db)

    socketio = SocketIO(logger=True, engineio_logger=True, cors_allowed_origins="*", Threaded=True, message_queue=app.config["REDIS_URL"])
    socketio.init_app(app)

    from api.tools import mailer
    mailer.init_app(app)

    return app