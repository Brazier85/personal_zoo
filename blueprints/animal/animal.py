from flask import current_app, render_template, request, redirect, url_for, flash, Blueprint
import os, json
from werkzeug.utils import secure_filename
from functions import *
from flask_weasyprint import HTML, render_pdf
from sqlalchemy.exc import SQLAlchemyError

animal_bp = Blueprint("animal", __name__, template_folder="templates")

@animal_bp.route("/<int:id>")
def animal(id):
    printing = request.args.get('print', default = 0)
    if printing == '1':
        limit = 10
    else:
        limit = 5

    location = 'animal'

    animal_data = get_ad(id)
    feeding_data = get_fd(None, id, limit)
    history_data = get_hd(None, id, limit)
    documents = get_docs('animal', id)

    weight_setting = get_setting("weight_type")
    try:
        #current_weight = db_fetch(f"SELECT text FROM history WHERE event='{weight_setting}' AND animal='{ id }' ORDER BY date DESC", False)[0]
        current_weight = History.query.filter(History.event==weight_setting).filter(History.animal==id).order_by(History.date.desc()).add_columns(History.text).first().text
        weight_number = float(current_weight.split(' ')[0].replace(',','.'))
    except:
        current_weight = "0"
        weight_number = 0
    
    feeding_size = ""
    setting_feeding_size = json.loads(get_setting("feeding_size"))
    if str(animal_data["art_id"]) in setting_feeding_size:
        # Calculate feeding size 
        if weight_number > 0:
            f_min_value = animal_data['f_min']
            f_max_value = animal_data['f_max']
            percent = lambda part, whole:float(whole) / 100 * float(part)
            feed_min = percent(f_min_value,weight_number)
            feed_max = percent(f_max_value,weight_number)
            feeding_size = f"Currently a feeding size between {feed_min:.0f}gr and {feed_max:.0f}gr ({f_min_value}% -> {f_max_value}%) is recommended!"

    if printing == '1':
        html = render_template('animal_print.html', animal=animal_data, feedings=feeding_data, history=history_data, location=location)
        return render_pdf(HTML(string=html), "", download_filename=f"{animal_data['name']}.pdf", automatic_download=False)
    else:
        return render_template('animal.html', animal=animal_data,
                               feedings=feeding_data, history=history_data,
                               location=location, current_weight=current_weight,
                               feeding_size=feeding_size, documents=documents)

@animal_bp.route('/add', methods=['POST','GET'])
def add():

    location = 'animal_add'
    if request.method == 'GET':
        return render_template('animal_add.html', location=location, animal_types=get_at(), feeding_types=get_ft(), terrariums=get_tr())
    
    elif request.method == 'POST':
        print(request.form)

        name = request.form['name']
        image = request.files['image']
        art = request.form['art']
        morph = request.form['morph']
        background_color = request.form['background-color']
        gender = request.form['gender']
        birth = request.form['birth']
        notes = request.form['notes']
        default_ft = request.form['dft']
        try:
            terrarium = request.form['terrarium']
        except:
            terrarium = 0

        # Check if an image was uploaded
        if image.filename != '':
            # Save the image to a folder
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(f"{UPLOAD_FOLDER}/animals", filename))
            else:
                flash('Invalid file. Please upload an image file.', 'error')
                return redirect(url_for('animal.add'))
        else:
            filename = "dummy.jpg"

        animal = Animal(name=name,
                        image=filename,
                        art=art,
                        morph=morph,
                        background_color=background_color,
                        gender=gender,
                        birth=birth,
                        notes=notes,
                        default_ft=default_ft,
                        terrarium=terrarium)
        db.session.add(animal)
        db.session.commit()

        flash('Data submitted successfully!', 'success')
        return redirect('/')

@animal_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    current_animal = Animal.query.filter(Animal.id==id).first()

    if request.method == 'GET':
        return render_template('animal_edit.html', data=current_animal, animal_types=get_at(), feeding_types=get_ft(), terrariums=get_tr())
    
    elif request.method == 'POST':
        current_animal.name = request.form['name']
        current_animal.art = request.form['art']
        current_animal.morph = request.form['morph']
        current_animal.background_color = request.form['background-color']
        current_animal.gender = request.form['gender']
        current_animal.birth = request.form['birth']
        current_animal.notes = request.form['notes']
        current_animal.default_ft = request.form['dft']
        current_animal.terrarium = request.form['terrarium']
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
                image.save(os.path.join(f"{UPLOAD_FOLDER}/animals", filename))
            else:
                # Invalid file format
                flash('Invalid file format. Please upload an image file.', 'error')
                return redirect(url_for('animal_edit', id=id))
        else:
            # No new image provided
            filename = current_image

        current_animal.image=filename
        current_animal.updated_date=datetime.date.today()

        db.session.add(current_animal)
        db.session.commit()

        flash('Data submitted successfully!', 'success')
        return redirect("/animal/"+str(id))

@animal_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    if request.method == 'POST':

        result = Animal.query.filter(Animal.id==id).add_columns(Animal.image).first()
        image_filename = result.image
        
        # Delete the image file
        if image_filename != 'dummy.jpg':
            image_path = os.path.join(f"{UPLOAD_FOLDER}/animals", str(image_filename))
            if os.path.exists(image_path):
                os.remove(image_path)

        animal = Animal.query.get_or_404(id)
        db.session.delete(animal)
        db.session.commit()

        feedings = Feeding.query.get_or_404(Feeding.animal==id)
        db.session.delete(feedings)
        db.session.commit()

        history = History.query.get_or_404(History.animal==id)
        db.session.delete(history)
        db.session.commit()

        flash('Animal deleted successfully!', 'success')

        return "", 200