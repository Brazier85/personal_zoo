import os

class Config(object):

    TESTING = False
    DEBUG = False
    
    # General config
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/uploads')
    SECRET_KEY = 'meine_tiere'
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/database.db')

class DevConfig(Config):      
    FLASK_ENV = "development"
    DEBUG = True

class ProdConfig(Config):
    FLASK_ENV = "production"
    DEBUG = False