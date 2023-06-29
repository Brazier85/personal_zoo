import os

class Config(object):
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/uploads')
    SECRET_KEY = 'meine_tiere'
    STATIC_FOLDER = 'static'
