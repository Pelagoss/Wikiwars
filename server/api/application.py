from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_migrate import Migrate

def create_app(app_name='WIKI_API'):
    app = Flask(app_name)
    app.config.from_object('api.config.BaseConfig')
    from api.api import api
    app.register_blueprint(api, url_prefix="/api")

    from api.models import db
    db.init_app(app)

    CORS(app, supports_credentials=True)

    migrate = Migrate()
    migrate.init_app(app, db)

    socketio = SocketIO(logger=True, engineio_logger=True, cors_allowed_origins="*", Threaded=True, message_queue=app.config["REDIS_URL"])
    socketio.init_app(app)

    from api.tools import mailer
    mailer.init_app(app)

    return app