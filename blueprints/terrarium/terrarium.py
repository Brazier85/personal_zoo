from flask import current_app, render_template, request, redirect, url_for, jsonify, flash, Blueprint
import os, json
from werkzeug.utils import secure_filename
from functions import *

terrarium_bp = Blueprint("terrarium", __name__, template_folder="templates")

@terrarium_bp.route("/<int:id>")
def terrarium(id):

    location = 'terrarium'

    terrarium_data = get_tr(id)

    return render_template('terrarium.html', location=location, terrarium=terrarium_data, details=get_td(None, terrarium_data["id"]), lamps=get_tl(None, terrarium_data["id"]))

@terrarium_bp.route('/add', methods=['POST','GET'])
def add():

    location = 'terrarium_add'
    if request.method == 'GET':
        return render_template('terrarium_add.html', location=location, terrarium_types=get_tt())
    
    elif request.method == 'POST':
        name = request.form.get('name')
        image = request.files['image']
        size = request.form['size']
        type = request.form['type']
        
        # Check if an image was uploaded
        if image.filename != '':
            # Save the image to a folder
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(f"{UPLOAD_FOLDER}/terrariums", filename))
            else:
                flash('Invalid file. Please upload an image file.', 'error')
                return redirect(url_for('terrarium.add'))
        else:
            filename = "dummy.jpg"

        terrarium = Terrarium(name=name,
                        image=filename,
                        size=size,
                        type=type)
        db.session.add(terrarium)
        db.session.commit()

        flash('Data submitted successfully!', 'success')
        return redirect('/')

@terrarium_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    current_terrarium = Terrarium.query.filter(Terrarium.id==id).first()

    if request.method == 'GET':
        return render_template('terrarium_edit.html', data=current_terrarium, terrarium_types=get_tt())
    
    elif request.method == 'POST':
        current_terrarium.name = request.form['name']
        current_terrarium.type = request.form['type']
        current_terrarium.size = request.form['size']
        current_terrarium.notes = request.form['notes']
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
                image.save(os.path.join(f"{UPLOAD_FOLDER}/terrariums", filename))
            else:
                # Invalid file format
                flash('Invalid file format. Please upload an image file.', 'error')
                return redirect(url_for('terrarium_edit', id=id))
        else:
            # No new image provided
            filename = current_image

        current_terrarium.image=filename

        db.session.add(current_terrarium)
        db.session.commit()

        flash('Data submitted successfully!', 'success')
        return redirect("/terrarium/"+str(id))

@terrarium_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    if request.method == 'POST':

        result = Terrarium.query.filter(Terrarium.id==id).add_columns(Terrarium.image).first()

        image_filename = result.image

        # Delete the image file
        if image_filename != 'dummy.png':
            image_path = os.path.join(f"{UPLOAD_FOLDER}/terrariums", str(image_filename))
            if os.path.exists(image_path):
                os.remove(image_path)

        terrarium = Terrarium.query.get_or_404(id)
        db.session.delete(terrarium)

        details = TerrariumDetails.query.get_or_404(TerrariumDetails.terrarium==id)
        db.session.delete(details)
        db.session.commit()

        flash('Terrarium deleted successfully!', 'success')

        return "", 200


@terrarium_bp.route('/detail/add/<int:id>', methods=['POST','GET'])
def detail_add(id):
    if request.method == 'GET':
        terrarium = Terrarium.query.filter(Terrarium.id==id).first()
        return render_template('detail_add.html', id=id, data=terrarium)
        
    elif request.method == 'POST':
        name = request.form['detail_name']
        text = request.form['detail_text']
        
        detail = TerrariumDetails(terrarium=id,
                            name=name,
                            text=text)
        db.session.add(detail)
        db.session.commit()

        flash('Added detail successfully!', 'success')
        current_app.logger.info("Added detail!")

        return redirect("/terrarium/"+str(id))
    
@terrarium_bp.route('/detail/edit/<int:id>', methods=['POST','GET'])
def detail_edit(id):

    detail = TerrariumDetails.query.filter(TerrariumDetails.id==id).first()

    if request.method == 'GET':
        return jsonify({'htmlresponse': render_template('detail_edit.html', data=detail)})
    
    elif request.method == 'POST':

        name = request.form['detail_name']
        text = request.form['detail_text']

        detail.count = name
        detail.text = text

        db.session.add(detail)
        db.session.commit()
        
        flash('Changes to detail saved!', 'success')
        current_app.logger.info(f"Modified detail with id: {id} !")
        return redirect("/terrarium/"+str(request.form['terrarium_id']))
    
@terrarium_bp.route('/detail/delete/<int:id>', methods=['POST'])
def detail_delete(id):
    if request.method == 'POST': 
        # Delete data into the database
        detail = TerrariumDetails.query.get_or_404(id)
        db.session.delete(detail)
        db.session.commit()
        flash('Deleted detail successfully!', 'success')
        current_app.logger.info(f"Deleted detail with id: {id} !")

        return "", 200
    
@terrarium_bp.route('/lamp/add/<int:id>', methods=['POST','GET'])
def lamp_add(id):
    if request.method == 'GET':
        terrarium = Terrarium.query.filter(Terrarium.id==id).first()
        return render_template('lamp_add.html', id=id, data=terrarium)
        
    elif request.method == 'POST':
        type = request.form['lamp_type']
        watt = request.form['lamp_watt']
        changed = datetime.datetime.strptime(request.form['lamp_changed'], '%Y-%m-%d')
        
        lamp = TerrariumLamps(terrarium=id,
                            type=type,
                            watt=watt,
                            changed=changed)
        db.session.add(lamp)
        db.session.commit()

        flash('Added lamp successfully!', 'success')
        current_app.logger.info("Added lamp!")

        return redirect("/terrarium/"+str(id))
    
@terrarium_bp.route('/lamp/edit/<int:id>', methods=['POST','GET'])
def lamp_edit(id):

    lamp = TerrariumLamps.query.filter(TerrariumLamps.id==id).first()

    if request.method == 'GET':
        return jsonify({'htmlresponse': render_template('lamp_edit.html', data=lamp)})
    
    elif request.method == 'POST':

        lamp.type = request.form['lamp_type']
        lamp.watt = request.form['lamp_watt']
        lamp.changed = datetime.datetime.strptime(request.form['lamp_changed'], '%Y-%m-%d')

        db.session.add(lamp)
        db.session.commit()
        
        flash('Changes to lamp saved!', 'success')
        current_app.logger.info(f"Modified lamp with id: {id} !")
        return redirect("/terrarium/"+str(request.form['terrarium_id']))
    
@terrarium_bp.route('/lamp/delete/<int:id>', methods=['POST'])
def lamp_delete(id):
    if request.method == 'POST': 
        # Delete data into the database
        lamp = TerrariumLamps.query.get_or_404(id)
        db.session.delete(lamp)
        db.session.commit()
        flash('Deleted lamp successfully!', 'success')
        current_app.logger.info(f"Deleted lamp with id: {id} !")

        return "", 200