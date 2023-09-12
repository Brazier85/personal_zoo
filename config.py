import os

class Config(object):

    TESTING = False
    DEBUG = False
    
    # General config
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/uploads')
    SECRET_KEY = '4a591941b7f9ce05833eeae0aca040e830072bbb067db5d3f3712b93babbba13'
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    
    # DB location
    DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/database.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+DATABASE
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(Config):      
    FLASK_ENV = "development"
    SECRET_KEY = '8ad5ab033fb63bbf3b17ccab423e7cce5b705254a420440e0012f05cf72583c0'
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
    BABEL_DEFAULT_LOCALE = 'de'

class ProdConfig(Config):
    FLASK_ENV = "production"
    DEBUG = False