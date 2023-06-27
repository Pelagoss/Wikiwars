from datetime import datetime, timedelta
import os

import jwt
from dotenv import load_dotenv, dotenv_values

env = os.getenv('APP_ENV', 'local')
dotenv_path = os.path.join(os.getcwd(), f'.env.{env}')

## Load .env file
load_dotenv()
## Load .env.{APP_ENV}
load_dotenv(dotenv_path, override=True)

class BaseConfig(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///wikiwars.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # used for encryption and session management
    SECRET_KEY = bytes(os.getenv("SECRET"), "latin-1")