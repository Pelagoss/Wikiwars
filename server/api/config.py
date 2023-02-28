class BaseConfig(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///wikiwars.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # used for encryption and session management
    SECRET_KEY = b'\xd4\xbd\x15\x84:U\xf5\xec\xf9\xcd"\x8d\xa6^lx'