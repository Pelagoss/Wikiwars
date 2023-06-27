import os

from dotenv import load_dotenv, dotenv_values

env = os.getenv('ENV', 'local')
dotenv_path = os.path.join(os.getcwd(), f'.env.{env}')

## Load .env file
configGlobal = dotenv_values()
## Load .env.{ENV}
config = dotenv_values(dotenv_path) | configGlobal
config = config | {
    'ENV': env,
    'DEBUG': True,
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///wikiwars.db',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    # used for encryption and session management
    'SECRET_KEY': bytes(config.get('SECRET_KEY'), "latin-1")
}

BaseConfig = type('BaseConfig', (object,), config)