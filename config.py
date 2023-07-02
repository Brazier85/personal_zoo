import os

from data.custom_settings import *

class Config(object):

    TESTING = False
    DEBUG = False
    
    # General config
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/uploads')
    SECRET_KEY = 'meine_tiere'
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/database.db')

    # Variable config
    if FEEDING_TYPES == None:
        FEEDING_TYPES =  ["Elefant","Kleinkind","Maus","Ratte","Wal"]
    else:
        FEEDING_TYPES = FEEDING_TYPES

    if EVENT_TYPES == None:
        EVENT_TYPES =  ["Häutung","Gewogen","Medizinisch","Sonstiges"]
    else:
        EVENT_TYPES = EVENT_TYPES

class DevConfig(Config):      
    FLASK_ENV = "development"
    DEBUG = True

class ProdConfig(Config):
    FLASK_ENV = "production"
    DEBUG = False