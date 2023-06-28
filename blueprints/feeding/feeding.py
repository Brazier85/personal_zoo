from flask import Flask, render_template, request, redirect, flash, jsonify, Blueprint
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
            return render_template('feeding_add.html', id=id)
        else:
            animal = db_fetch(f"SELECT name FROM animals WHERE id={ id }", False)
            return render_template('feeding_add_external.html', id=id, animal=animal[0])
        
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

        flash('Added feeding successfully!')

        return redirect("/animal/"+str(id))
    
@feeding_bp.route('/edit/<int:id>', methods=['POST','GET'])
def edit(id):
    if request.method == 'GET':
        return jsonify({'htmlresponse': render_template('feeding_edit.html', data=db_fetch(f"SELECT * FROM feeding WHERE  id={ id }", False))})
    
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
        
        flash('Changes to feeding saved!')
        return redirect("/animal/"+str(animal_id))
    
@feeding_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    if request.method == 'POST': 
        # Delete data into the database
        db_update(f"DELETE FROM feeding WHERE id={ id }")
        flash('Deleted feeding successfully!')

        return "", 200