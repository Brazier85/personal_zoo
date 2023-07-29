from flask import current_app, render_template, request, redirect, flash, jsonify, send_from_directory, Blueprint
from werkzeug.utils import secure_filename
from datetime import datetime
from functions import *
import uuid

document_bp = Blueprint("document", __name__, template_folder="templates")

@document_bp.route('/download/<int:id>')
def download(id):
    file = Document.query.filter(Document.id==id).first()
    return send_from_directory(f"{UPLOAD_FOLDER}/documents", file.filename)

@document_bp.route('/get_all/<int:id>', methods=['POST','GET'])
def get_all(id):
    if request.method == 'GET':
        less = request.args.get('less')
        if (less):
            feedings=get_fd(None,id,5)
        else:
            feedings=get_fd(None,id)
        return render_template('document_all.html', feedings=feedings)

@document_bp.route('/add/<string:target>/<int:id>', methods=['POST','GET'])
def add(target, id):
    if request.method == 'GET':
        if target == 'animal':
            animal = Animal.query.add_columns(Animal.id, Animal.name).filter(Animal.id==id).one()
            return render_template('document_add.html', id=id, animal=animal)
        elif target == 'terrarium':
            terrarium = Terrarium.query.add_columns(Terrarium.id, Terrarium.name).filter(Terrarium.id==id).one()
            return render_template('document_add.html', id=id, terrarium=terrarium)
            
    elif request.method == 'POST':
        form_file = request.files['file']
        name = request.form['file_name']
        if target == 'animal':
            animal_id = id
            terrarium_id = 'NULL'
        elif target == 'terrarium':
            terrarium_id = id
            animal_id = 'NULL'

        # Check if an image was uploaded
        if form_file.filename != '':
            # Save the image to a folder
            if form_file and allowed_file(form_file.filename):
                filename = f"{uuid.uuid4().hex[:8]}_{secure_filename(form_file.filename)}"
                form_file.save(os.path.join(f"{UPLOAD_FOLDER}/documents", filename))
            else:
                flash('Invalid file. Please upload an pdf file.', 'danger')
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
    
@document_bp.route('/edit/<int:id>', methods=['POST','GET'])
def edit(id):

    document = Document.query.filter(Document.id==id).first()

    if request.method == 'GET':
        return jsonify({'htmlresponse': render_template('document_edit.html', data=document)})
    
    elif request.method == 'POST':

        document.name = request.form['file_name']

        db.session.add(document)
        db.session.commit()
        
        flash('Changes to document saved!', 'success')
        current_app.logger.info(f"Modified document with id: {id} !")

        if int(document.animal_id) > 0:
            return redirect("/animal/"+str(document.animal_id))
        else:
            return redirect("/terrarium/"+str(document.terrarium_id))
    
@document_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
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