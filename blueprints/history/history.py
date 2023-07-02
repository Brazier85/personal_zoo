from flask import current_app, render_template, request, redirect, flash, jsonify, Blueprint
from functions import *

history_bp = Blueprint("history", __name__, template_folder="templates")

@history_bp.route('/get_all/<int:id>', methods=['POST','GET'])
def get_all(id):
    if request.method == 'GET':
        history_data = db_fetch(f"SELECT * FROM history WHERE animal={ id } ORDER BY date DESC")
        formatted_history_data = date_eu(history_data,4)
        return render_template('history_all.html', history=formatted_history_data)
    

@history_bp.route('/add/<int:id>', methods=['POST','GET'])
def add(id):
    if request.method == 'GET':
        return render_template('history_add.html', id=id, event_types=current_app.config['EVENT_TYPES'])

    elif request.method == 'POST':
        history = request.form
        event = history['history_event']
        text = history['history_text']
        date = history['history_date']
        
        query = "INSERT INTO history " \
                    "(animal, event, text, date)" \
                    f"VALUES ('{id}', '{event}', '{text}', '{date}')"
        db_update(query)

        flash('Added event/action successfully!', 'success')
        current_app.logger.info("Added history!")

        return redirect("/animal/"+str(id))
    
@history_bp.route('/multi', methods=['POST','GET'])
def multi_add():
    if request.method == 'GET':
        animals = db_fetch(f"SELECT id, name FROM animals ORDER BY name DESC")
        return render_template('history_multi_add.html', animals=animals, event_types=current_app.config['EVENT_TYPES'])

    elif request.method == 'POST':
        history = request.form
        animals = history.getlist('animals')
        event = history['history_event']
        text = history['history_text']
        date = history['history_date']
        
        for animal in animals:
            query = "INSERT INTO history " \
                        "(animal, event, text, date)" \
                        f"VALUES ('{animal}', '{event}', '{text}', '{date}')"
            db_update(query)

        flash('Added event/action successfully!', 'success')
        current_app.logger.info("Added history!")

        return redirect("/")
    
@history_bp.route('/edit/<int:id>', methods=['POST','GET'])
def edit(id):
    if request.method == 'GET':
        return jsonify({'htmlresponse': render_template('history_edit.html', data=db_fetch(f"SELECT * FROM history WHERE  id={ id }", False), event_types=current_app.config['EVENT_TYPES'])})
    
    elif request.method == 'POST':
        history = request.form
        event = history['history_event']
        text = history['history_text']
        date = history['history_date']
        animal_id = history['animal_id']

        query = "UPDATE history " \
                    f"SET event='{event}', text='{text}', date='{date}'" \
                    f"WHERE id='{ id }'"
        db_update(query)

        flash('Changes to history saved!', 'success')
        current_app.logger.info(f"Modified history with id: {id} !")
        return redirect("/animal/"+str(animal_id))

@history_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    if request.method == 'POST': 
        # Delete data into the database
        db_update(f"DELETE FROM history WHERE id={ id }")

        flash('Deleted history successfully!', 'success')
        current_app.logger.info(f"Deleted history with id: {id} !")

        return "", 200