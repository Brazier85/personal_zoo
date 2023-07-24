from flask import Flask, render_template, request, send_from_directory, flash, redirect
from flask_qrcode import QRcode
from flask_mail import Mail, Message
import os
import logging
from logging.config import dictConfig
from werkzeug.exceptions import HTTPException
import traceback
from datetime import datetime
from flask_apscheduler import APScheduler

# Imports
from models import *
from functions import *
from momentjs import momentjs

# Import Blueprints
from blueprints.animal.animal import animal_bp
from blueprints.terrarium.terrarium import terrarium_bp
from blueprints.feeding.feeding import feeding_bp
from blueprints.history.history import history_bp
from blueprints.settings.settings import settings_bp
from blueprints.maintenance.maintenance import maintenance_bp


# Environment file
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
mail = Mail(app)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

# Logging
logging.getLogger('werkzeug').disabled = True
dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s | %(module)s >>> %(message)s",
                "datefmt": "%B %d, %Y %H:%M:%S %Z",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["console"]},
    }
)

# Configuration
if os.getenv("PZOO_FLASK_ENV") == 'dev':
    app.logger.warning(f"App running in mode: { os.environ.get('PZOO_FLASK_ENV') }")
    app.config.from_object('config.DevConfig')
else:
    app.logger.info(f"App running in mode: { os.environ.get('PZOO_FLASK_ENV') }")
    app.config.from_object('config.ProdConfig')

# Init DB
db.init_app(app)

with app.app_context():
    db.create_all()

QRcode(app)
# MomentJS
app.jinja_env.globals['momentjs'] = momentjs

# Blueprints
app.register_blueprint(animal_bp, url_prefix="/animal")
app.register_blueprint(feeding_bp, url_prefix="/feeding")
app.register_blueprint(history_bp, url_prefix="/history")
app.register_blueprint(settings_bp, url_prefix="/settings")
app.register_blueprint(terrarium_bp, url_prefix="/terrarium")
app.register_blueprint(maintenance_bp, url_prefix="/maintenance")

@app.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return render_template("error_html.html", e=e)

    app.logger.error(e)
    # now you're handling non-HTTP exceptions only
    return render_template("error_generic.html", e=str(e), traceback=traceback.format_exc())

@app.after_request
def logAfterRequest(response):

    app.logger.info(
        "path: %s | method: %s | status: %s | size: %s",
        request.path,
        request.method,
        response.status,
        response.content_length,
    )

    return response

@app.template_filter(name='linebreaksbr')
def linebreaksbr_filter(text):
    try:
        return text.replace('\n', '<br \>')
    except:
        return text

@app.template_filter(name='fix_date')
def fix_date_filter(text):
    try:
        new_text = datetime.strptime(text, '%Y-%m-%d').strftime('%d.%m.%Y')
        return new_text
    except:
        text = text

    try:
        new_text = text.strftime('%d.%m.%Y')
        return new_text
    except:
        text = text

    return text

# Check every minute for notifications
@scheduler.task('cron', id='send_notifications', minute='*')
def send_notifications():
    send_mail()

# Main route
@app.route('/')
def home():

    location = 'home'  # Set the current location (e.g., 'Home')

    # Create the table if it doesn't exist
    insert_defaults()

    order = request.cookies.get('animal_order')
    if order == None:
        order = "name"

    return render_template('home.html', animals=get_ad(), feeding_types=get_ft(), terrariums=get_tr(), location=location)

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

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    else:
        return send_from_directory(app.config['UPLOAD_FOLDER'], 'dummy.jpg')

# Do update stuff
@app.route('/update')
def old_update():
    return redirect("/maintenance/update")


###############
#     MAIN    #
###############

if __name__ == '__main__':
    create_folders()
    app.run(host="0.0.0.0")
