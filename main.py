from flask import Flask, render_template, request, send_from_directory, flash, redirect, g
from flask_qrcode import QRcode
from flask_mail import Mail, Message
from flask_login import (
    LoginManager,
    current_user
)
import os
import logging
from logging.config import dictConfig
from werkzeug.exceptions import HTTPException
import traceback
from datetime import datetime
from flask_apscheduler import APScheduler
from flask_bcrypt import Bcrypt
from flask_babel import Babel

# Imports
from models import *
from functions import *
from momentjs import momentjs

# Import Blueprints
from blueprints.animal.animal import animal_bp
from blueprints.api.api import api_bp
from blueprints.document.document import document_bp
from blueprints.terrarium.terrarium import terrarium_bp
from blueprints.feeding.feeding import feeding_bp
from blueprints.history.history import history_bp
from blueprints.settings.settings import settings_bp
from blueprints.maintenance.maintenance import maintenance_bp
from blueprints.accounts.accounts import accounts_bp

# Feeding Form
from blueprints.feeding.forms import FeedingMultiForm

# Define AP
app = Flask(__name__)

# Environment file
from dotenv import load_dotenv
load_dotenv()

# App configuration
if os.getenv("PZOO_FLASK_ENV") == 'dev':
    app.logger.warning(f"App running in mode: { os.environ.get('PZOO_FLASK_ENV') }")
    app.config.from_object('config.DevConfig')
else:
    app.logger.info(f"App running in mode: { os.environ.get('PZOO_FLASK_ENV') }")
    app.config.from_object('config.ProdConfig')

mail = Mail(app)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

# Logging
app.logger.setLevel(logging.INFO)
dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s | %(module)s >>> %(message)s",
                "datefmt": "%B %d, %Y %H:%M:%S %Z"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default",
            },
            "error_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "default",
                "filename": app.config['APPLICATION_LOG_PATH'] + "/error.log",
                "maxBytes": 10000,
                "backupCount": 10,
                "delay": "True",
                'level': 'ERROR',
            }
        },
        "root": {
            "level": "INFO",
            "handlers": ['console',  'error_file']
        }
    }
)
logging.getLogger('werkzeug').disabled = True

# Login management
login_manager = LoginManager()
login_manager.init_app(app)

bcrypt = Bcrypt(app)

def get_locale():
    # if a user is logged in, use the locale from the user settings
    if current_user.lang is not None:
        return current_user.lang
    return request.accept_languages.best_match(['de', 'en'])

def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone
    

babel = Babel(app, locale_selector=get_locale, timezone_selector=get_timezone)

# Init DB
db.init_app(app)

session = []

with app.app_context():
    db.create_all()

#QRCodes
QRcode(app)

# MomentJS
app.jinja_env.globals['momentjs'] = momentjs

# Blueprints
app.register_blueprint(accounts_bp, url_prefix="/account")
app.register_blueprint(animal_bp, url_prefix="/animal")
app.register_blueprint(api_bp, url_prefix="/api/v1")
app.register_blueprint(document_bp, url_prefix="/document")
app.register_blueprint(feeding_bp, url_prefix="/feeding")
app.register_blueprint(history_bp, url_prefix="/history")
app.register_blueprint(maintenance_bp, url_prefix="/maintenance")
app.register_blueprint(settings_bp, url_prefix="/settings")
app.register_blueprint(terrarium_bp, url_prefix="/terrarium")

# Error handler
@app.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        print(e.get_response())
        if e.code == 401:
            return render_template("error_401.html")
        else:
            return render_template("error_html.html", e=e)

    app.logger.error(e)
    # now you're handling non-HTTP exceptions only
    return render_template("error_generic.html", e=str(e), traceback=traceback.format_exc())

# Logging
@app.after_request
def AfterRequest(response):

    IGNORE_REQUESTS_CODES = [304]

    if response.status_code not in IGNORE_REQUESTS_CODES:
        app.logger.info(
            "path: %s | method: %s | status: %s",
            request.path,
            request.method,
            response.status
        )
    return response

# New line to br
@app.template_filter(name='linebreaksbr')
def linebreaksbr_filter(text):
    try:
        return text.replace('\n', '<br />')
    except:
        return text

# Check every minute for notifications
@scheduler.task('cron', id='send_notifications', minute='*')
def send_notifications():
    send_mail()

# Load users
@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()

# Check if PW is okay
def check_pw(hash, pw):
    if bcrypt.check_password_hash(hash, pw):
        return True
    else:
        return False
    
# Gen new pw hash
def gen_hash(pw):
    return bcrypt.generate_password_hash(pw)

# Main route
@app.route('/')
def home():

    location = 'home'  # Set the current location (e.g., 'Home')

    # Create the table if it doesn't exist
    insert_defaults()

    # Detect if mobile user
    user_agent = request.headers.get("User-Agent")
    user_agent = user_agent.lower()
    phones = ["android", "iphone"]

    if any(phone in user_agent for phone in phones):
        return render_template('home_mobile.html', animals=get_ad(), terrariums=get_tr(), settings=get_setting(), location=location)
    else:
        return render_template('home.html', animals=get_ad(), terrariums=get_tr(), settings=get_setting(), location=location)

# Route for printing
@app.route('/print')
@app.route('/print/<int:id>')
def print_data(id=None):
    location = 'print'

    if id:
        animal_data = get_ad(id)
    else:
        animal_data = get_ad()

    feed_url = f"{request.url_root}feeding/add/"

    return render_template('print.html', animals=animal_data, location=location, feed_url=feed_url)

# Routes to get uploaded files
@app.route('/uploads/<folder>/<filename>')
@app.route('/uploads/<filename>')
def uploaded_file(folder='', filename=''):
    if folder != '':
        path = f"{app.config['UPLOAD_FOLDER']}/{folder}"
    else:
        path = app.config['UPLOAD_FOLDER']

    # Check if image exists
    file_path = os.path.join(path, filename)
    if os.path.exists(file_path):
        return send_from_directory(path, filename)
    else:
        return send_from_directory(path, 'dummy.jpg')

# Do update stuff
@app.route('/update')
def old_update():
    return redirect("/maintenance/update")

# Login
@app.route('/login')
def to_login():
    return redirect("/account/login")


###############
#     MAIN    #
###############

if __name__ == '__main__':
    create_folders()
    app.run(host="0.0.0.0")
