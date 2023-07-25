from flask import current_app, render_template, request, redirect, flash, jsonify, Blueprint
from datetime import datetime
from functions import *

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
def add(id):
    if request.method == 'GET':
        external = request.args.get('external')
        animal = Animal.query.add_columns(Animal.name, Animal.default_ft).filter(Animal.id==id).one()
        if external is None:
            return render_template('feeding_add.html', id=id, animal=animal, feeding_types=get_ft())
        else:
            return render_template('feeding_add_external.html', id=id, animal=animal, feeding_types=get_ft())
        
    elif request.method == 'POST':
        feeding = request.form
        count = feeding['feeding_count']
        type = feeding['feeding_type']
        unit = feeding['feeding_unit']
        date = feeding['feeding_date']

        date = datetime.datetime.strptime(date, '%Y-%m-%d')
        
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
    
@feeding_bp.route('/multi', methods=['POST','GET'])
def multi_add():
    if request.method == 'GET':
        # get animals
        terrarium = request.args.get('terrarium')
        animals = Animal.query.add_columns(Animal.id, Animal.name).all()

        if terrarium is None:
            return render_template('feeding_multi_add.html', animals=animals, feeding_types=get_ft(), terrariums=get_tr(), location="multi_feeding")
        else:
            return render_template('feeding_multi_add.html', animals=animals, feeding_types=get_ft(), terrariums=get_tr(), t_select=terrarium, location="multi_feeding")
        
    elif request.method == 'POST':
        feeding = request.form
        animals = feeding.getlist('animals')
        terrariums = feeding.getlist('terrariums')
        count = feeding['feeding_count']
        ftype = feeding['feeding_type']
        unit = feeding['feeding_unit']
        date = feeding['feeding_date']

        date = datetime.datetime.strptime(date, '%Y-%m-%d')

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
    
    
@feeding_bp.route('/edit/<int:id>', methods=['POST','GET'])
def edit(id):

    feeding = Feeding.query.filter(Feeding.id==id).first()

    if request.method == 'GET':
        return jsonify({'htmlresponse': render_template('feeding_edit.html', data=feeding, feeding_types=get_ft())})
    
    elif request.method == 'POST':

        feeding_data = request.form
        count = feeding_data['feeding_count']
        type = feeding_data['feeding_type']
        unit = feeding_data['feeding_unit']
        date = feeding_data['feeding_date']
        animal_id = feeding_data['animal_id']

        date = datetime.datetime.strptime(date, '%Y-%m-%d')

        feeding.count = count
        feeding.type = type
        feeding.unit = unit
        feeding.date = date
        feeding.animal = animal_id

        db.session.add(feeding)
        db.session.commit()
        
        flash('Changes to feeding saved!', 'success')
        current_app.logger.info(f"Modified feeding with id: {id} !")
        return redirect("/animal/"+str(animal_id))
    
@feeding_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    if request.method == 'POST': 
        # Delete data into the database
        feeding = Feeding.query.get_or_404(id)
        db.session.delete(feeding)
        db.session.commit()
        flash('Deleted feeding successfully!', 'success')
        current_app.logger.info(f"Deleted feeding with id: {id} !")

        return "", 200