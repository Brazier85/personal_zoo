from flask import Flask, render_template, request, send_from_directory, flash, redirect
from flask_qrcode import QRcode
import os
import logging
from logging.config import dictConfig
from werkzeug.exceptions import HTTPException
import traceback

# Imports
from functions import *
from momentjs import momentjs

# Import Blueprints
from blueprints.animal.animal import animal_bp
from blueprints.feeding.feeding import feeding_bp
from blueprints.history.history import history_bp
from blueprints.settings.settings import settings_bp

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
# MomentJS
app.jinja_env.globals['momentjs'] = momentjs

# Blueprints
app.register_blueprint(animal_bp, url_prefix="/animal")
app.register_blueprint(feeding_bp, url_prefix="/feeding")
app.register_blueprint(history_bp, url_prefix="/history")
app.register_blueprint(settings_bp, url_prefix="/settings")

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
    return text.replace('\n', '<br \>')

@app.template_filter(name='fix_date')
def fix_date_filter(text):
    try:
        text = datetime.strptime(text, '%Y-%m-%d').strftime('%d.%m.%Y')
        return text
    except:
        return text

# Main route
@app.route('/')
def home():

    location = 'home'  # Set the current location (e.g., 'Home')

    # Create the table if it doesn't exist
    create_tables()
    insert_defaults()

    data = db_fetch("SELECT * FROM animals ORDER BY name ASC")

    return render_template('home.html', data=data, location=location)

# Route for printing
@app.route('/print')
@app.route('/print/<int:id>')
def print_data(id=None):
    location = 'print'

    if id:
        data = db_fetch(f"SELECT * FROM animals WHERE id='{id}'")
    else:
        data = db_fetch("SELECT * FROM animals ORDER BY name")

    feed_url = f"{request.url_root}feeding/add/"

    return render_template('print.html', data=data, location=location, feed_url=feed_url)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    else:
        return send_from_directory(app.config['UPLOAD_FOLDER'], 'dummy.jpg')
    
# Do update stuff
@app.route('/update')
def update():

    error = ""

    print("Running database updates....")
    exists = None
    exists = db_fetch("SELECT * FROM settings WHERE setting='feeding_size'", False)
    if exists == None:
        print("Insert new setting feeding_size to database")
        query = "INSERT INTO settings " \
                "(setting, value, name, description)" \
                f"VALUES ('feeding_size','[\"1\"]','Feeding Size','Show feeding size for animal type!')"
        db_update(query)

    print("Remove old column")
    try:
        query= "ALTER TABLE animal_type DROP COLUMN note"
        db_update(query)
    except Exception as e:
        print(f"Error: {e} -> Remove old column")
        error = error + f"Remove old column 'note' -> Error: {e}\n"

    print("Add new columns")
    try:
        query= "ALTER TABLE animal_type ADD COLUMN f_min INT DEFAULT 0"
        db_update(query)
    except Exception as e:
        print(f"Error: {e}")
        error = error + f"Add f_min -> Error: {e}\n"
    
    try:
        query= "ALTER TABLE animal_type ADD COLUMN f_max INT DEFAULT 0"
        db_update(query)
    except Exception as e:
        print(f"Error: {e}")
        error = error + f"Add f_max -> Error: {e}\n"

    try:
        query = f"UPDATE animal_type SET f_min='0', f_max='0' WHERE f_min IS NULL OR f_max IS NULL"
        db_update(query)
    except Exception as e:
        print(f"Error: {e}")
        error = error + f"Add f_max -> Error: {e}\n"

    if error != "":
        flash(f"<strong>Error while doing update!</strong>\n\n{error}", 'danger')
    else:
        flash("Update done!", 'success')
    return redirect('/')


###############
#     MAIN    #
###############

if __name__ == '__main__':
    app.run(host="0.0.0.0")
