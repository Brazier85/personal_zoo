from flask import current_app, render_template, request, redirect, url_for, flash, Blueprint
import os
from werkzeug.utils import secure_filename
from functions import *
from flask_weasyprint import HTML, render_pdf

animal_bp = Blueprint("animal", __name__, template_folder="templates")

@animal_bp.route("/<int:id>")
def animal(id):
    printing = request.args.get('print', default = 0)
    if printing == '1':
        limit = 10
    else:
        limit = 5

    location = 'animal'

    animal_data = db_fetch(f"SELECT * FROM animals WHERE id={ id }", False)
    formatted_animal_data = date_eu(animal_data,10)

    feeding_data = db_fetch(f"SELECT f.id as id, f.animal, ft.name, f.count, f.weight, date FROM feeding f LEFT JOIN feeding_type ft ON f.type = ft.id WHERE animal={ id } ORDER BY date DESC LIMIT { limit }")
    formatted_feeding_data = date_eu(feeding_data,5)

    history_data = db_fetch(f"SELECT h.id, h.animal, ht.name, h.text, h.date FROM history h LEFT JOIN history_type ht ON h.event = ht.id WHERE animal={ id } ORDER BY date DESC LIMIT { limit }")
    formatted_history_data = date_eu(history_data,4)

    weight_setting = get_setting("weight_type")
    try:
        current_weight = db_fetch(f"SELECT text FROM history WHERE event='{weight_setting}' AND animal='{ id }' ORDER BY date DESC", False)[0]
    except:
        current_weight = "0 gr"

    if printing == '1':
        html = render_template('animal_print.html', data=formatted_animal_data, feedings=formatted_feeding_data, history=formatted_history_data, location=location)
        return render_pdf(HTML(string=html), "", download_filename=f"{animal_data[1]}.pdf", automatic_download=False)
        #return html
    else:
        return render_template('animal.html', data=formatted_animal_data, feedings=formatted_feeding_data, history=formatted_history_data, location=location, current_weight=current_weight)

@animal_bp.route('/add', methods=['POST','GET'])
def add():

    location = 'add'
    if request.method == 'GET':
        return render_template('animal_add.html', location=location)
    
    elif request.method == 'POST':
        name = request.form.get('name')
        image = request.files['image']
        art = request.form['art']
        morph = request.form['morph']
        background_color = request.form['background-color']
        gender = request.form['gender']
        birth = request.form['birth']
        notes = request.form['notes']

        # Check if an image was uploaded
        if image.filename != '':
            # Save the image to a folder
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(UPLOAD_FOLDER, filename))
            else:
                flash('Invalid file. Please upload an image file.', 'error')
                return redirect(url_for('animal.add'))
        else:
            filename = "dummy.jpg"

        query = "INSERT INTO animals" \
                    "(name, image, art, morph, background_color, gender, birth, notes)" \
                    f"VALUES ('{ name }', '{ filename }', '{ art }', '{ morph }', '{ background_color }', '{ gender }', '{ birth }', '{ notes }')"
        db_update(query)

        flash('Data submitted successfully!', 'success')
        return redirect('/')

@animal_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'GET':
        return render_template('animal_edit.html', data=db_fetch(f"SELECT * FROM animals WHERE id={ id }", False))
    
    elif request.method == 'POST':
        name = request.form['name']
        art = request.form['art']
        morph = request.form['morph']
        background_color = request.form['background-color']
        gender = request.form['gender']
        birth = request.form['birth']
        notes = request.form['notes']
        current_image = request.form['current_image']

        # Check if a new image file is provided
        if 'image' in request.files:
            image = request.files['image']
            if image.filename == '':
                # No new image provided
                filename = current_image
            elif allowed_file(image.filename):
                # New valid image provided
                filename = secure_filename(image.filename)
                image.save(os.path.join(UPLOAD_FOLDER, filename))
            else:
                # Invalid file format
                flash('Invalid file format. Please upload an image file.', 'error')
                return redirect(url_for('animal_edit', id=id))
        else:
            # No new image provided
            filename = current_image

        query = "UPDATE animals " \
                    f"SET name='{ name }', art='{ art }', morph='{ morph }', background_color='{ background_color }'," \
                    f"gender='{ gender }', birth='{ birth }', notes='{ notes }', image='{ filename }', updated_date=CURRENT_DATE " \
                    f"WHERE id='{ id }'"
        db_update(query)

        flash('Data submitted successfully!', 'success')
        return redirect("/animal/"+str(id))

@animal_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    if request.method == 'POST':

        result = db_fetch(f"SELECT image FROM animals WHERE id={ id }")

        if result:
            image_filename = result[0]
        else:
            flash('Record not found!', 'error')
            return redirect('/')

        # Delete the image file
        if image_filename != 'dummy.png':
            if image_filename:
                image_path = os.path.join(UPLOAD_FOLDER, str(image_filename))
                if os.path.exists(image_path):
                    os.remove(image_path)

        db_update(f"DELETE FROM animals WHERE id={ id }")

        flash('Animal deleted successfully!', 'success')

        return "", 200
