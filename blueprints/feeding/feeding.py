from flask import current_app, render_template, request, redirect, flash, jsonify, Blueprint
from functions import *

feeding_bp = Blueprint("feeding", __name__, template_folder="templates")

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
            return render_template('feeding_add.html', id=id, feeding_types=current_app.config['FEEDING_TYPES'])
        else:
            animal = db_fetch(f"SELECT name FROM animals WHERE id={ id }", False)
            return render_template('feeding_add_external.html', id=id, animal=animal[0], feeding_types=current_app.config['FEEDING_TYPES'])
        
    elif request.method == 'POST':
        feeding = request.form
        count = feeding['feeding_count']
        type = feeding['feeding_type']
        weight = feeding['feeding_weight']
        date = feeding['feeding_date']
        

        query = "INSERT INTO feeding " \
                    "(animal, type, count, weight, date)" \
                    f"VALUES ('{id}', '{type}', '{count}', '{weight}', '{date}')"
        db_update(query)

        flash('Added feeding successfully!', 'success')
        current_app.logger.info("Added feeding!")

        return redirect("/animal/"+str(id))
    
@feeding_bp.route('/multi', methods=['POST','GET'])
def multi_add():
    if request.method == 'GET':
        # get animals
        animals = db_fetch(f"SELECT id, name FROM animals ORDER BY name DESC")
        return render_template('feeding_multi_add.html', animals=animals, feeding_types=current_app.config['FEEDING_TYPES'])
        
    elif request.method == 'POST':
        feeding = request.form
        animals = feeding.getlist('animals')
        count = feeding['feeding_count']
        type = feeding['feeding_type']
        weight = feeding['feeding_weight']
        date = feeding['feeding_date']

        for animal in animals:
            query = "INSERT INTO feeding " \
                        "(animal, type, count, weight, date)" \
                        f"VALUES ('{animal}', '{type}', '{count}', '{weight}', '{date}')"
            db_update(query)

        flash('Added multi feeding successfully!', 'success')
        current_app.logger.info("Added multi feeding!")

        return redirect("/")
    
    
@feeding_bp.route('/edit/<int:id>', methods=['POST','GET'])
def edit(id):
    if request.method == 'GET':
        return jsonify({'htmlresponse': render_template('feeding_edit.html', data=db_fetch(f"SELECT * FROM feeding WHERE  id={ id }", False), feeding_types=current_app.config['FEEDING_TYPES'])})
    
    elif request.method == 'POST':
        feeding = request.form
        count = feeding['feeding_count']
        type = feeding['feeding_type']
        weight = feeding['feeding_weight']
        date = feeding['feeding_date']
        animal_id = feeding['animal_id']

        query = "UPDATE feeding " \
                    f"SET type='{type}', count='{count}', weight='{weight}', date='{date}'" \
                    f"WHERE id='{ id }'"
        db_update(query)
        
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