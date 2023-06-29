from flask import Flask, render_template, request, send_from_directory
from flask_qrcode import QRcode

# Imports
from config import Config
from functions import *

# Import Blueprints
from blueprints.animal.animal import animal_bp
from blueprints.feeding.feeding import feeding_bp
from blueprints.history.history import history_bp

app = Flask(__name__)
# Configuration
app.config.from_object(Config)

QRcode(app)

# Blueprints
app.register_blueprint(animal_bp, url_prefix="/animal")
app.register_blueprint(feeding_bp, url_prefix="/feeding")
app.register_blueprint(history_bp, url_prefix="/history")

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
    app.run(host="0.0.0.0",debug=True)
