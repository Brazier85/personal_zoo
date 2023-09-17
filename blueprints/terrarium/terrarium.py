from flask import current_app, render_template, request, redirect, url_for, jsonify, flash, Blueprint
import os, json
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
from functions import *

from .forms import TerrariumForm, EquipmentForm, LampsForm, EventsForm

terrarium_bp = Blueprint("terrarium", __name__, template_folder="templates")

@terrarium_bp.route("/<int:id>")
def terrarium(id):

    location = 'terrarium'

    terrarium_data = get_tr(id)

    return render_template('terrarium.html', location=location, settings=get_setting(), animals=get_ad(None, terrarium_data["id"]), terrarium=terrarium_data, equipment=get_te(None, terrarium_data["id"]), lamps=get_tl(None, terrarium_data["id"]), terrarium_history=get_thd(None, terrarium_data["id"]))

@terrarium_bp.route('/add', methods=['POST','GET'])
def add():

    location = 'terrarium_add'
    UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']

    form = TerrariumForm(CombinedMultiDict((request.files, request.form)))

    form.type.choices = [(i.id, i.name) for i in get_tt()]
    
    if form.validate_on_submit():
        name = form.name.data
        size = form.size.data
        type = form.type.data
        notes = form.notes.data
        
        if form.image.data:
            image = form.image.data
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
        else:
            filename = "dummy.jpg"

        terrarium = Terrarium(name=name,
                        image=filename,
                        size=size,
                        type=type,
                        notes=notes)
        db.session.add(terrarium)
        db.session.commit()

        flash('Data submitted successfully!', 'success')
        return redirect('/')
    
    return render_template('terrarium_add.html', location=location, form=form)

@terrarium_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    current_terrarium = Terrarium.query.filter(Terrarium.id==id).first()
    UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']

    form = TerrariumForm(CombinedMultiDict((request.files, request.form)), obj=current_terrarium)

    form.type.choices = [(i.id, i.name) for i in get_tt()]

    if form.validate_on_submit():
        current_terrarium.name = form.name.data
        current_terrarium.type = form.type.data
        current_terrarium.size = form.size.data
        current_terrarium.notes = form.notes.data
        old_image = current_terrarium.image

        # Check if a new image file is provided
        if 'image' in request.files:
            image = request.files['image']
            if image.filename == '':
                # No new image provided
                filename = old_image
            elif allowed_file(image.filename):
                # New valid image provided
                filename = secure_filename(image.filename)
                image.save(os.path.join(f"{UPLOAD_FOLDER}/terrariums", filename))
                # Delete old file
                if str(current_terrarium.image) != 'dummy.jpg':
                    try:
                        file_path = os.path.join(f"{UPLOAD_FOLDER}/terrariums", str(current_terrarium.image))
                        if os.path.exists(file_path):
                            os.remove(file_path)
                    except:
                        print(f"Could not delete old file: {current_terrarium.image}")
            else:
                # Invalid file format
                flash('Invalid file format. Please upload an image file.', 'error')
                return redirect(url_for('terrarium_edit', id=id))
        else:
            # No new image provided
            filename = current_terrarium.image

        current_terrarium.image=filename

        db.session.add(current_terrarium)
        db.session.commit()

        flash('Data submitted successfully!', 'success')
        return redirect("/terrarium/"+str(id))
    
    return render_template('terrarium_edit.html', data=current_terrarium, form=form)

@terrarium_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
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
        db.session.commit()

        details = TerrariumEquipment.query.get_or_404(TerrariumEquipment.terrarium==id)
        db.session.delete(details)
        db.session.commit()

        flash('Terrarium deleted successfully!', 'success')

        return "", 200


@terrarium_bp.route('/equipment/add/<int:id>', methods=['POST','GET'])
def equipment_add(id):

    form = EquipmentForm(request.form)

    if form.validate_on_submit():
        name = form.name.data
        text = form.text.data
        
        equipment = TerrariumEquipment(terrarium=id,
                            name=name,
                            text=text)
        db.session.add(equipment)
        db.session.commit()

        flash('Added equipment successfully!', 'success')
        current_app.logger.info("Added equipment!")

        return redirect("/terrarium/"+str(id))
    
    terrarium = Terrarium.query.filter(Terrarium.id==id).first()
    return render_template('equipment_add.html', id=id, data=terrarium, form=form)
    
@terrarium_bp.route('/equipment/edit/<int:id>', methods=['POST','GET'])
def equipment_edit(id):

    equipment = TerrariumEquipment.query.filter(TerrariumEquipment.id==id).first()
    form = EquipmentForm(request.form, obj=equipment)
  
    if form.validate_on_submit():

        equipment.name = form.name.data
        equipment.text = form.text.data

        db.session.add(equipment)
        db.session.commit()
        
        flash('Changes to equipment saved!', 'success')
        current_app.logger.info(f"Modified equipment with id: {id} !")
        return redirect("/terrarium/"+str(request.form['terrarium_id']))
    
    return jsonify({'htmlresponse': render_template('equipment_edit.html', data=equipment, form=form)})
    
@terrarium_bp.route('/equipment/delete/<int:id>', methods=['POST'])
def equipment_delete(id):
    if request.method == 'POST': 
        # Delete data into the database
        detail = TerrariumEquipment.query.get_or_404(id)
        db.session.delete(detail)
        db.session.commit()
        flash('Deleted equipment successfully!', 'success')
        current_app.logger.info(f"Deleted equipment with id: {id} !")

        return "", 200
    
@terrarium_bp.route('/lamp/add/<int:id>', methods=['POST','GET'])
def lamp_add(id):

    form = LampsForm(request.form)

    if form.validate_on_submit():
        type = form.type.data
        watt = form.watt.data
        position = form.position.data
        changed = form.changed.data
        
        lamp = TerrariumLamps(terrarium=id,
                            type=type,
                            watt=watt,
                            position=position,
                            changed=changed)
        db.session.add(lamp)
        db.session.commit()

        flash('Added lamp successfully!', 'success')
        current_app.logger.info("Added lamp!")

        return redirect("/terrarium/"+str(id))
    
    terrarium = Terrarium.query.filter(Terrarium.id==id).first()
    return render_template('lamp_add.html', id=id, data=terrarium, form=form)
    
@terrarium_bp.route('/lamp/edit/<int:id>', methods=['POST','GET'])
def lamp_edit(id):

    lamp = TerrariumLamps.query.filter(TerrariumLamps.id==id).first()

    form = LampsForm(request.form, obj=lamp)
  
    if form.validate_on_submit():

        lamp.type = form.type.data
        lamp.watt = form.watt.data
        lamp.position = form.position.data
        lamp.changed = form.changed.data

        db.session.add(lamp)
        db.session.commit()
        
        flash('Changes to lamp saved!', 'success')
        current_app.logger.info(f"Modified lamp with id: {id} !")
        return redirect("/terrarium/"+str(lamp.terrarium))
    
    return jsonify({'htmlresponse': render_template('lamp_edit.html', data=lamp, form=form)})
    
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
    
@terrarium_bp.route('/history/get_all/<int:id>', methods=['POST','GET'])
def terrarium_history_get_all(id):
    if request.method == 'GET':
        less = request.args.get('less')
        if (less):
            terrarium_history=get_thd(None,id,5)
        else:
            terrarium_history=get_thd(None,id)
        return render_template('t_history_all.html', terrarium_history=terrarium_history)
    
@terrarium_bp.route('/history/add/<int:id>', methods=['POST','GET'])
def terrarium_history_add(id):

    form = EventsForm(request.form)

    form.event.choices = [(i.id, i.name) for i in get_htt()]

    if form.validate_on_submit():
        event = form.event.data
        text = form.text.data
        date = form.date.data

        event = TerrariumHistory(terrarium=id,
                            event=event,
                            text=text,
                            date=date)
        db.session.add(event)
        db.session.commit()
        
        flash('Added terrarium event/action successfully!', 'success')
        current_app.logger.info("Added terrarium history!")

        return redirect("/terrarium/"+str(id))
    
    return render_template('t_history_add.html', id=id, form=form)
    
@terrarium_bp.route('/history/edit/<int:id>', methods=['POST','GET'])
def terrarium_history_edit(id):

    event = TerrariumHistory.query.filter(TerrariumHistory.id==id).first()

    form = EventsForm(request.form, obj=event)

    form.event.choices = [(i.id, i.name) for i in get_htt()]

    if form.validate_on_submit():
        event.event = form.event.data
        event.text = form.text.data
        event.date = form.date.data
        
        db.session.add(event)
        db.session.commit()

        flash('Changes to terrarium history saved!', 'success')
        current_app.logger.info(f"Modified terrarium history with id: {id} !")
        return redirect("/terrarium/"+str(event.terrarium))
    
    return jsonify({'htmlresponse': render_template('t_history_edit.html', data=event, form=form)})

@terrarium_bp.route('/history/delete/<int:id>', methods=['POST'])
def terrarium_history_delete(id):
    if request.method == 'POST': 
        # Delete data into the database
        event = TerrariumHistory.query.get_or_404(id)
        db.session.delete(event)
        db.session.commit()

        flash('Deleted terrarium history successfully!', 'success')
        current_app.logger.info(f"Deleted terrarium history with id: {id} !")

        return "", 200