from flask import current_app, render_template, request, redirect, flash, jsonify, Blueprint
from datetime import datetime
from functions import *

feeding_bp = Blueprint("feeding", __name__, template_folder="templates")


@feeding_bp.route('/get_units/<int:id>', methods=['POST','GET'])
def get_units(id):
    if request.method == 'GET':
        value = request.args.get('value', default="")
        unit_data = db_fetch(f"SELECT unit, detail from feeding_type WHERE id={ id }", False)
        return render_template('feeding_unit.html', unit_data=unit_data, value=value)

@feeding_bp.route('/get_all/<int:id>', methods=['POST','GET'])
def get_all(id):
    if request.method == 'GET':
        feeding_data= db_fetch(f"SELECT f.id as id, f.animal, ft.name, f.count, f.unit, date, ft.unit, ft.detail FROM feeding f LEFT JOIN feeding_type ft ON f.type = ft.id WHERE animal={ id } ORDER BY date DESC")
        return render_template('feeding_all.html', feedings=feeding_data)

@feeding_bp.route('/get_qr/<int:id>')
def qr_code(id):
    animal = db_fetch(f"SELECT name FROM animals WHERE id={ id }", False)
    feed_url = f"{request.url_root}feeding/add/{ id }?external"
    return render_template('feeding_qr.html', id=id, animal=animal[0], feed_url=feed_url)

@feeding_bp.route('/add/<int:id>', methods=['POST','GET'])
def add(id):
    if request.method == 'GET':
        external = request.args.get('external')
        if external is None:
            return render_template('feeding_add.html', id=id, feeding_types=get_ft())
        else:
            animal = db_fetch(f"SELECT name FROM animals WHERE id={ id }", False)
            return render_template('feeding_add_external.html', id=id, animal=animal[0], feeding_types=get_ft())
        
    elif request.method == 'POST':
        feeding = request.form
        count = feeding['feeding_count']
        type = feeding['feeding_type']
        unit = feeding['feeding_unit']
        date = feeding['feeding_date']
        

        query = "INSERT INTO feeding " \
                    "(animal, type, count, unit, date)" \
                    f"VALUES ('{id}', '{type}', '{count}', '{unit}', '{date}')"
        db_update(query)

        flash('Added feeding successfully!', 'success')
        current_app.logger.info("Added feeding!")

        return redirect("/animal/"+str(id))
    
@feeding_bp.route('/multi', methods=['POST','GET'])
def multi_add():
    if request.method == 'GET':
        # get animals
        animals = Animal.query.add_columns(Animal.id, Animal.name).all()
        return render_template('feeding_multi_add.html', animals=animals, feeding_types=get_ft(), location="multi_feeding")
        
    elif request.method == 'POST':
        feeding = request.form
        animals = feeding.getlist('animals')
        count = feeding['feeding_count']
        type = feeding['feeding_type']
        unit = feeding['feeding_unit']
        date = feeding['feeding_date']

        for animal in animals:
            query = "INSERT INTO feeding " \
                        "(animal, type, count, unit, date)" \
                        f"VALUES ('{animal}', '{type}', '{count}', '{unit}', '{date}')"
            db_update(query)

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

        date = datetime.strptime(date, '%Y-%m-%d')

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
        db_update(f"DELETE FROM feeding WHERE id={ id }")
        flash('Deleted feeding successfully!', 'success')
        current_app.logger.info(f"Deleted feeding with id: {id} !")

        return "", 200