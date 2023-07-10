from flask import current_app, render_template, request, redirect, url_for, flash, Blueprint
import os, json
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

    animal_data = db_fetch(f"SELECT a.id as id, a.name, at.name as art, a.morph, a.gender, a.birth, a.notes, a.image, a.background_color, a.created_date, a.updated_date, at.id as aid FROM animals a LEFT JOIN animal_type at ON a.art = at.id WHERE a.id={ id }", False)

    feeding_data = db_fetch(f"SELECT f.id as id, f.animal, ft.name, f.count, f.weight, date FROM feeding f LEFT JOIN feeding_type ft ON f.type = ft.id WHERE animal={ id } ORDER BY date DESC LIMIT { limit }")

    history_data = db_fetch(f"SELECT h.id, h.animal, ht.name, h.text, h.date FROM history h LEFT JOIN history_type ht ON h.event = ht.id WHERE animal={ id } ORDER BY date DESC LIMIT { limit }")

    weight_setting = get_setting("weight_type")
    try:
        current_weight = db_fetch(f"SELECT text FROM history WHERE event='{weight_setting}' AND animal='{ id }' ORDER BY date DESC", False)[0]
        weight_number = float(current_weight.split(' ')[0].replace(',','.'))
    except:
        current_weight = "0"
        weight_number = 0
    
    feeding_size = ""
    setting_feeding_size = json.loads(get_setting("feeding_size"))
    if str(animal_data[11]) in setting_feeding_size:
        print("true")
        # Calculate feeding size 
        if weight_number > 0:
            print("Weight bigger than zero")
            print("Python")
            percent = lambda part, whole:float(whole) / 100 * float(part)
            feed_min = percent(10,weight_number)
            feed_max = percent(20,weight_number)
            feeding_size = f"Currently a feeding size between {feed_min:.0f}gr and {feed_max:.0f}gr (10% -> 20%) is recommended!"

    if printing == '1':
        html = render_template('animal_print.html', data=animal_data, feedings=feeding_data, history=history_data, location=location)
        return render_pdf(HTML(string=html), "", download_filename=f"{animal_data[1]}.pdf", automatic_download=False)
        #return html
    else:
        return render_template('animal.html', data=animal_data, feedings=feeding_data, history=history_data, location=location, current_weight=current_weight, feeding_size=feeding_size)

@animal_bp.route('/add', methods=['POST','GET'])
def add():

    location = 'add'
    if request.method == 'GET':
        return render_template('animal_add.html', location=location, animal_types=get_at())
    
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
        return render_template('animal_edit.html', data=db_fetch(f"SELECT * FROM animals WHERE id={ id }", False), animal_types=get_at())
    
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
        db_update(f"DELETE FROM feeding WHERE animal={ id }")
        db_update(f"DELETE FROM history WHERE animal={ id }")

        flash('Animal deleted successfully!', 'success')

        return "", 200
