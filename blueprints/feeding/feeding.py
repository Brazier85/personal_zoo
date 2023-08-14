from flask import current_app, render_template, request, redirect, flash, jsonify, url_for, Blueprint
from flask_login import login_required
from datetime import datetime
from functions import *

from .forms import FeedingForm, FeedingMultiForm

feeding_bp = Blueprint("feeding", __name__, template_folder="templates")


@feeding_bp.route('/get_units/<int:id>', methods=['POST','GET'])
def get_units(id):
    if request.method == 'GET':
        value = request.args.get('value', default="")
        unit_data = FeedingType.query.filter(FeedingType.id==id).add_columns(FeedingType.unit, FeedingType.detail).first()
        return render_template('feeding_unit.html', unit_data=unit_data, value=value)

@feeding_bp.route('/get_all/<int:id>', methods=['POST','GET'])
def get_all(id):
    if request.method == 'GET':
        less = request.args.get('less')
        if (less):
            feedings=get_fd(None,id,5)
        else:
            feedings=get_fd(None,id)
        return render_template('feeding_all.html', feedings=feedings)

@feeding_bp.route('/get_qr/<int:id>')
def qr_code(id):
    animal = Animal.query.filter(Animal.id==id).add_columns(Animal.id, Animal.name).first()
    feed_url = f"{request.url_root}feeding/add/{ id }?external"
    return render_template('feeding_qr.html', id=id, animal=animal.name, feed_url=feed_url)

@feeding_bp.route('/add/<int:id>', methods=['POST','GET'])
@login_required
def add(id):

    form = FeedingForm(request.form)

    # Adding select values
    form.type.choices = [(i.id, i.name) for i in get_ft()]

    if form.validate_on_submit():
        feeding = request.form
        count = form.count.data
        type = form.type.data
        unit = form.unit.data
        date = form.date.data
        
        feeding = Feeding(animal=id,
                            type=type,
                            count=count,
                            unit=unit,
                            date=date)
        db.session.add(feeding)
        db.session.commit()

        flash('Added feeding successfully!', 'success')
        current_app.logger.info("Added feeding!")

        return redirect("/animal/"+str(id))
    
    
    external = request.args.get('external')
    animal = Animal.query.add_columns(Animal.name, Animal.default_ft).filter(Animal.id==id).one()
    if external is None:
        return render_template('feeding_add.html', id=id, form=form, target=url_for("feeding.add", id=id), dft=animal.default_ft)
    else:
        return render_template('feeding_add_external.html', id=id, animal=animal.name, form=form, target=url_for("feeding.add", id=id), dft=animal.default_ft)
    
@feeding_bp.route('/multi', methods=['POST','GET'])
@login_required
def multi_add():

    terrarium = request.args.get('terrarium')

    form = FeedingMultiForm(request.form)

    # Adding select values
    form.type.choices = [(i.id, i.name) for i in get_ft()]
    form.animals.choices = [(i.id, i.name) for i in Animal.query.add_columns(Animal.id, Animal.name).all()]
    form.terrariums.choices = [(i["id"], i["name"]) for i in get_tr()]

    if form.validate_on_submit():
        animals = form.animals.data
        terrariums = form.terrariums.data
        count = form.count.data
        ftype = form.type.data
        unit = form.unit.data
        date = form.date.data

        # Get terrarium animals
        if terrariums != []:
            for terrarium in terrariums:
                additional_animals = Animal.query.filter(Animal.terrarium == terrarium).add_columns(Animal.id).all()
                for animal in additional_animals:
                    if str(animal.id) not in animals:
                        animals.append(f"{animal.id}")

        for animal in animals:
            feeding = Feeding(animal=animal,
                            type=ftype,
                            count=count,
                            unit=unit,
                            date=date)
            db.session.add(feeding)
            db.session.commit()

        flash('Added multi feeding successfully!', 'success')
        current_app.logger.info("Added multi feeding!")

        return redirect("/")
    
    

    if terrarium is None:
        return render_template('feeding_multi_add.html', form=form, location="multi_feeding")
    else:
        return render_template('feeding_multi_add.html', form=form, terrarium=terrarium, location="multi_feeding")
    
    
@feeding_bp.route('/edit/<int:id>', methods=['POST','GET'])
@login_required
def edit(id):

    feeding = Feeding.query.filter(Feeding.id==id).first()

    form = FeedingForm(request.form, obj=feeding)

    # Adding select values
    form.type.choices = [(i.id, i.name) for i in get_ft()]

    if form.validate_on_submit():

        feeding.count = form.count.data
        feeding.type = form.type.data
        feeding.unit = form.unit.data
        feeding.date = form.date.data

        db.session.add(feeding)
        db.session.commit()
        
        flash('Changes to feeding saved!', 'success')
        current_app.logger.info(f"Modified feeding with id: {id} !")
        return redirect("/animal/"+str(feeding.animal))
    
    return jsonify({'htmlresponse': render_template('feeding_edit.html', form=form, target=url_for("feeding.edit", id=id), id=id)})
    
@feeding_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    if request.method == 'POST': 
        # Delete data into the database
        feeding = Feeding.query.get_or_404(id)
        db.session.delete(feeding)
        db.session.commit()
        flash('Deleted feeding successfully!', 'success')
        current_app.logger.info(f"Deleted feeding with id: {id} !")

        return "", 200