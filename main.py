from flask import Flask, render_template, request, send_from_directory
from flask_qrcode import QRcode
import os
import logging
from logging.config import dictConfig

# Imports
from functions import *

# Import Blueprints
from blueprints.animal.animal import animal_bp
from blueprints.feeding.feeding import feeding_bp
from blueprints.history.history import history_bp

app = Flask(__name__)

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
        "root": {"level": "DEBUG", "handlers": ["console"]},
    }
)

# Configuration
if os.environ.get('FLASK_ENV') == 'dev':
    app.logger.warning(f"App running in mode: { os.environ.get('FLASK_ENV') }")
    app.config.from_object('config.DevConfig')
else:
    app.logger.info(f"App running in mode: { os.environ.get('FLASK_ENV') }")
    app.config.from_object('config.ProdConfig')


QRcode(app)

# Blueprints
app.register_blueprint(animal_bp, url_prefix="/animal")
app.register_blueprint(feeding_bp, url_prefix="/feeding")
app.register_blueprint(history_bp, url_prefix="/history")

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

# Main route
@app.route('/')
def home():

    location = 'home'  # Set the current location (e.g., 'Home')

    # Create the table if it doesn't exist
    create_tables()

    data = db_fetch("SELECT * FROM animals ORDER BY name ASC")
    formatted_data = date_eu(data, 10)

    return render_template('home.html', data=formatted_data, location=location)

# Route for printing
@app.route('/print')
@app.route('/print/<int:id>')
def print_data(id=None):
    location = 'print'

    if id:
        data = db_fetch(f"SELECT * FROM animals WHERE id='{id}'")
    else:
        data = db_fetch("SELECT * FROM animals ORDER BY name")

    # Convert the date string to the desired format (DD.MM.YYYY)
    formatted_data = date_eu(data, 9)
    feed_url = f"{request.url_root}feeding/add/"

    return render_template('print.html', data=formatted_data, location=location, feed_url=feed_url)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

###############
#     MAIN    #
###############

if __name__ == '__main__':
    app.run(host="0.0.0.0")
