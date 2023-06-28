from flask import Flask, render_template, request, redirect, flash, jsonify, Blueprint
from functions import *

history_bp = Blueprint("history", __name__, template_folder="templates")

@history_bp.route('/add/<int:id>', methods=['POST','GET'])
def add(id):
    if request.method == 'GET':
        return render_template('history_add.html', id=id)

    elif request.method == 'POST':
        history = request.form
        event = history['history_event']
        text = history['history_text']
        date = history['history_date']
        
        query = "INSERT INTO history " \
                    "(animal, event, text, date)" \
                    f"VALUES ('{id}', '{event}', '{text}', '{date}')"
        db_update(query)

        flash('Added event/action successfully!')

        return redirect("/animal/"+str(id))
    
@history_bp.route('/edit/<int:id>', methods=['POST','GET'])
def edit(id):
    if request.method == 'GET':
        return jsonify({'htmlresponse': render_template('history_edit.html', data=db_fetch(f"SELECT * FROM history WHERE  id={ id }", False))})
    
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

        flash('Changes to history saved!')
        return redirect("/animal/"+str(animal_id))

@history_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    if request.method == 'POST': 
        # Delete data into the database
        db_update(f"DELETE FROM history WHERE id={ id }")

        flash('Deleted history successfully!')

        return "", 200