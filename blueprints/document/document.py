from flask import current_app, render_template, request, redirect, flash, jsonify, send_from_directory, url_for, Blueprint
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
from flask_login import login_required
from datetime import datetime
from functions import *
import uuid

from .forms import DocumentForm

document_bp = Blueprint("document", __name__, template_folder="templates")

@document_bp.route('/download/<int:id>')
@login_required
def download(id):
    UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
    file = Document.query.filter(Document.id==id).first()
    return send_from_directory(f"{UPLOAD_FOLDER}/documents", file.filename)

@document_bp.route('/add/<string:target>/<int:id>', methods=['POST','GET'])
@login_required
def add(target, id):
    UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']

    form = DocumentForm(CombinedMultiDict((request.files, request.form)))

    if form.validate_on_submit():
        form_file = form.filename.data
        name = form.name.data
        if target == 'animal':
            animal_id = id
            terrarium_id = 'NULL'
        elif target == 'terrarium':
            terrarium_id = id
            animal_id = 'NULL'

        print(f"animal: {animal_id}")
        print(f"terrarium: {terrarium_id}")

        # Check if an image was uploaded
        if form_file.filename != '':
            # Save the image to a folder
            if form_file and allowed_file(form_file.filename):
                filename = f"{uuid.uuid4().hex[:8]}_{secure_filename(form_file.filename)}"
                form_file.save(os.path.join(f"{UPLOAD_FOLDER}/documents", filename))
            else:
                flash('Invalid file type. Please upload an valid file. (pdf, png, jpg)', 'danger')
                if target == 'animal':
                    return redirect("/animal/"+str(animal_id))
                elif target == 'terrarium':
                    return redirect("/terrarium/"+str(animal_id))
        
            file = Document(name=name,
                            filename=filename,
                            animal_id=animal_id,
                            terrarium_id=terrarium_id)
            db.session.add(file)
            db.session.commit()

            flash('Added document successfully!', 'success')
            current_app.logger.info("Added document!")  
        else:
            flash('No file found!', 'danger')
            current_app.logger.info("Error adding document!")

        if target == 'animal':
            return redirect("/animal/"+str(animal_id))
        elif target == 'terrarium':
            return redirect("/terrarium/"+str(animal_id))
        
    if target == 'animal':
        animal = Animal.query.add_columns(Animal.id, Animal.name).filter(Animal.id==id).one()
        return render_template('document_add.html', id=id, animal=animal, form=form, target="animal")
    elif target == 'terrarium':
        terrarium = Terrarium.query.add_columns(Terrarium.id, Terrarium.name).filter(Terrarium.id==id).one()
        return render_template('document_add.html', id=id, terrarium=terrarium, form=form, target="terrarium")
    
@document_bp.route('/edit/<int:id>', methods=['POST','GET'])
@login_required
def edit(id):
    UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']

    document = Document.query.filter(Document.id==id).first()

    form = DocumentForm(CombinedMultiDict((request.files, request.form)), obj=document)

    if form.validate_on_submit():

        document.name = form.name.data
        print(f"animal: {document.animal_id}")
        print(f"terrarium: {document.terrarium_id}")

        # Check if a new image file is provided
        if form.filename.data:
            file = form.filename.data
            if file.filename == '':
                # No new file provided
                filename = document.filename
            elif allowed_file(file.filename):
                # New valid file provided
                filename = f"{uuid.uuid4().hex[:8]}_{secure_filename(file.filename)}"
                file.save(os.path.join(f"{UPLOAD_FOLDER}/documents", filename))
                # Delete old file
                try:
                    file_path = os.path.join(f"{UPLOAD_FOLDER}/documents", str(document.filename))
                    if os.path.exists(file_path):
                        os.remove(file_path)
                except:
                    print(f"Could not delete old file: {document.filename}")
            else:
                # Invalid file format
                flash('Invalid file format. Please upload an image file.', 'error')
                if int(document.animal_id) > 0:
                    return redirect("/animal/"+str(document.animal_id))
                else:
                    return redirect("/terrarium/"+str(document.terrarium_id))
        else:
            filename = document.filename
            
        document.filename = filename

        db.session.add(document)
        db.session.commit()
        
        flash('Changes to document saved!', 'success')
        current_app.logger.info(f"Modified document with id: {id} !")

        if int(document.animal_id) > 0:
            return redirect("/animal/"+str(document.animal_id))
        else:
            return redirect("/terrarium/"+str(document.terrarium_id))
        
    return jsonify({'htmlresponse': render_template('document_edit.html', form=form, id=id)})
    
@document_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
    if request.method == 'POST': 
        document = Document.query.get_or_404(id)

        # Delete the file
        file_path = os.path.join(f"{UPLOAD_FOLDER}/documents", str(document.filename))
        if os.path.exists(file_path):
            os.remove(file_path)

        # Delete data into the database
        db.session.delete(document)
        db.session.commit()
        flash('Deleted document successfully!', 'success')
        current_app.logger.info(f"Deleted document with id: {id} !")

        return "", 200