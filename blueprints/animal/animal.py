from flask import current_app, render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_required
import os, json
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
from functions import *
from flask_weasyprint import HTML, render_pdf
from sqlalchemy.exc import SQLAlchemyError

from .forms import AnimalForm

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
                                feeding_size=feeding_size, settings=get_setting(),
                                documents=documents)

@animal_bp.route('/add', methods=['POST','GET'])
@login_required
def add():

    location = 'animal_add'

    form = AnimalForm(CombinedMultiDict((request.files, request.form)))

    # Adding select values
    form.art.choices = [(i.id, i.name) for i in get_at()]
    form.default_ft.choices = [(i.id, i.name) for i in get_ft()]
    form.terrarium.choices = [(i["id"], i["name"]) for i in get_tr()]
    form.gender.choices = [('female', 'Female'),('male', 'Male'),('other', 'Other')]


    if form.validate_on_submit():
        name = form.name.data
        art = form.art.data
        morph = form.morph.data
        background_color = form.background_color.data
        gender = form.gender.data
        birth = form.birth.data
        notes = form.notes.data
        default_ft = form.default_ft.data
        try:
            terrarium = form.terrarium.data
        except:
            terrarium = 0

        print(f"Image: {form.image.data}")

        # Check if an image was uploaded
        if form.image.data:
            image = form.image.data
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

    return render_template('animal_add.html', form=form, location=location, target="/animal/add/")


@animal_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):

    current_animal = Animal.query.filter(Animal.id==id).first()

    form = AnimalForm(CombinedMultiDict((request.files, request.form)), obj=current_animal)

    # Adding select values
    form.art.choices = [(i.id, i.name) for i in get_at()]
    form.default_ft.choices = [(i.id, i.name) for i in get_ft()]
    form.terrarium.choices = [(i["id"], i["name"]) for i in get_tr()]
    form.gender.choices = [('female', 'Female'),('male', 'Male'),('other', 'Other')]

    if form.validate_on_submit():
        current_animal.name = form.name.data
        current_animal.art = form.art.data
        current_animal.morph = form.morph.data
        current_animal.background_color = form.background_color.data
        current_animal.gender = form.gender.data
        current_animal.birth = form.birth.data
        current_animal.notes = form.notes.data
        current_animal.default_ft = form.default_ft.data
        current_animal.terrarium = form.terrarium.data
        new_image = form.image.data

        # Check if a new image file is provided
        if 'image' in request.files:
            image = request.files['image']
            if image.filename == '':
                # No new image provided
                filename = new_image
            elif allowed_file(image.filename):
                # New valid image provided
                filename = secure_filename(image.filename)
                image.save(os.path.join(f"{UPLOAD_FOLDER}/animals", filename))
                # Delete old file
                if str(current_animal.image) != 'dummy.jpg':
                    try:
                        file_path = os.path.join(f"{UPLOAD_FOLDER}/animals", str(current_animal.image))
                        if os.path.exists(file_path):
                            os.remove(file_path)
                    except:
                        print(f"Could not delete old file: {current_animal.image}")
            else:
                # Invalid file format
                flash('Invalid file format. Please upload an image file.', 'error')
                return redirect(url_for('animal_edit', id=id))
        else:
            # No new image provided
            filename = current_animal.image

        current_animal.image=filename
        current_animal.updated_date=datetime.date.today()

        db.session.add(current_animal)
        db.session.commit()

        flash('Data submitted successfully!', 'success')
        return redirect("/animal/"+str(id))
    
    return render_template('animal_edit.html', form=form, animal=current_animal, target="/animal/edit/"+str(id))

@animal_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
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