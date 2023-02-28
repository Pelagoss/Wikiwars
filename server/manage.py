from flask.cli import FlaskGroup, with_appcontext
from flask_migrate import Migrate

from api.application import create_app
from api.models import db, User, Game, u_g

app = create_app()

migrate = Migrate()
migrate.init_app(app, db)

cli = FlaskGroup(app)

# enable python shell with application context
@with_appcontext
def shell_ctx():
    return dict(app=app,
                db=db,
                User=User,
                Game=Game)

if __name__ == '__main__':
    cli()