from flask import current_app, render_template, request, redirect, flash, jsonify, Blueprint
from functions import *
import json

settings_bp = Blueprint("settings", __name__, template_folder="templates")

@settings_bp.route("/")
def settings():

    location = 'settings'

    settings = get_setting()

    return render_template('settings.html', feeding_types=get_ft(), history_types=get_ht(), ht=get_ht(), settings=get_setting(), animal_types=get_at(), location=location)

@settings_bp.route('/edit', methods=['POST','GET'])
def edit():
    if request.method == 'GET':
        return 200
    
    elif request.method == 'POST':
        settings = request.form
        weight = settings["weight"]
        feeding_size = settings.getlist('feeding_size')

        print(f"Feeding size: {feeding_size}")

        # Weight setting
        query = f"UPDATE settings SET value='{weight}' WHERE setting='weight_type'"
        db_update(query)

        # Feeding size
        query = f"UPDATE settings SET value='{json.dumps(feeding_size)}' WHERE setting='feeding_size'"
        db_update(query)

        flash('Settings saved!', 'success')
        current_app.logger.info("Settings saved")
        return redirect("/settings")
    

@settings_bp.route('/ft_edit/<int:id>', methods=['POST','GET'])
def ft_edit(id):
    if request.method == 'GET':
        return jsonify({'htmlresponse': render_template('ft_edit.html', data=db_fetch(f"SELECT * FROM feeding_type WHERE id={ id }", False))})
    
    elif request.method == 'POST':
        data = request.form
        name = data['ft_name']
        note = data['ft_note']

        query = "UPDATE feeding_type " \
                    f"SET name='{name}', note='{note}'"\
                    f"WHERE id='{ id }'"
        db_update(query)

        flash('Changes to feeding type saved!', 'success')
        current_app.logger.info(f"Modified feeding type with id: {id} !")
        return redirect("/settings")
    
@settings_bp.route('/ft_add', methods=['POST','GET'])
def ft_add():
    if request.method == 'GET':
        return render_template('ft_add.html')

    elif request.method == 'POST':
        data = request.form
        name = data['ft_name']
        note = data['ft_note']
        
        query = "INSERT INTO feeding_type " \
                    "(name, note)" \
                    f"VALUES ('{name}', '{note}')"
        db_update(query)

        flash('Added feed type successfully!', 'success')
        current_app.logger.info("Added feed type !")

        return redirect("/settings")
    
@settings_bp.route('/ft_delete/<int:id>', methods=['POST'])
def ft_delete(id):
    if request.method == 'POST': 
        # Delete data into the database
        db_update(f"DELETE FROM feeding_type WHERE id={ id }")

        flash('Deleted feeding type successfully!', 'success')
        current_app.logger.info(f"Deleted feeding type with id: {id} !")

        return "", 200
    
@settings_bp.route('/ht_edit/<int:id>', methods=['POST','GET'])
def ht_edit(id):
    if request.method == 'GET':
        return jsonify({'htmlresponse': render_template('ht_edit.html', data=db_fetch(f"SELECT * FROM history_type WHERE id={ id }", False))})
    
    elif request.method == 'POST':
        history = request.form
        name = history['ht_name']
        note = history['ht_note']

        query = "UPDATE history_type " \
                    f"SET name='{name}', note='{note}'" \
                    f"WHERE id='{ id }'"
        db_update(query)

        flash('Changes to history type saved!', 'success')
        current_app.logger.info(f"Modified history type with id: {id} !")
        return redirect("/settings")
    
@settings_bp.route('/ht_add', methods=['POST','GET'])
def ht_add():
    if request.method == 'GET':
        return render_template('ht_add.html')

    elif request.method == 'POST':
        data = request.form
        name = data['ht_name']
        note = data['ht_note']
        
        query = "INSERT INTO history_type " \
                    "(name, note)" \
                    f"VALUES ('{name}', '{note}')"
        db_update(query)

        flash('Added history type successfully!', 'success')
        current_app.logger.info("Added history type !")

        return redirect("/settings")
    
@settings_bp.route('/ht_delete/<int:id>', methods=['POST'])
def ht_delete(id):
    if request.method == 'POST': 
        # Delete data into the database
        db_update(f"DELETE FROM history_type WHERE id={ id }")

        flash('Deleted history type successfully!', 'success')
        current_app.logger.info(f"Deleted history type with id: {id} !")

        return "", 200
    
@settings_bp.route('/at_edit/<int:id>', methods=['POST','GET'])
def at_edit(id):
    if request.method == 'GET':
        return jsonify({'htmlresponse': render_template('at_edit.html', data=db_fetch(f"SELECT * FROM animal_type WHERE id={ id }", False))})
    
    elif request.method == 'POST':
        data = request.form
        name = data['at_name']
        f_min = data['at_f_min']
        f_max = data['at_f_max']

        query = "UPDATE animal_type " \
                    f"SET name='{name}', f_min='{f_min}', f_max='{f_max}'" \
                    f"WHERE id='{ id }'"
        db_update(query)

        flash('Changes to animal type saved!', 'success')
        current_app.logger.info(f"Modified animal type with id: {id} !")
        return redirect("/settings")
    
@settings_bp.route('/at_add', methods=['POST','GET'])
def at_add():
    if request.method == 'GET':
        return render_template('at_add.html')

    elif request.method == 'POST':
        data = request.form
        name = data['at_name']
        f_min = data['at_f_min']
        f_max = data['at_f_max']
        
        query = "INSERT INTO animal_type " \
                    "(name, f_min, f_max)" \
                    f"VALUES ('{name}', '{f_min}', '{f_max}')"
        db_update(query)

        flash('Added animal type successfully!', 'success')
        current_app.logger.info("Added animal type !")

        return redirect("/settings")
    
@settings_bp.route('/at_delete/<int:id>', methods=['POST'])
def at_delete(id):
    if request.method == 'POST': 
        # Delete data into the database
        db_update(f"DELETE FROM animal_type WHERE id={ id }")

        flash('Deleted animal type successfully!', 'success')
        current_app.logger.info(f"Deleted animal type with id: {id} !")

        return "", 200