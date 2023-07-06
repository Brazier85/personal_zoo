from flask import current_app, render_template, request, redirect, flash, jsonify, Blueprint
from functions import *

settings_bp = Blueprint("settings", __name__, template_folder="templates")

@settings_bp.route("/")
def settings():

    location = 'settings'

    return render_template('settings.html', feeding_types=get_ft(), history_types=get_ht(), ht=get_ht(), settings=get_setting(), location=location)

@settings_bp.route('/edit', methods=['POST','GET'])
def edit():
    if request.method == 'GET':
        return 200
    
    elif request.method == 'POST':
        settings = request.form
        weight = settings["weight"]

        query = f"UPDATE settings SET setting='{weight}' WHERE name='weight_type'"
        db_update(query)

        flash('Settings saved!', 'success')
        current_app.logger.info("Settings saved")
        return redirect("/settings")
    

@settings_bp.route('/ft_edit/<int:id>', methods=['POST','GET'])
def ft_edit(id):
    if request.method == 'GET':
        return jsonify({'htmlresponse': render_template('ft_edit.html', data=db_fetch(f"SELECT * FROM feeding_type WHERE id={ id }", False))})
    
    elif request.method == 'POST':
        history = request.form
        name = history['ft_name']
        note = history['ft_note']

        query = "UPDATE feeding_type " \
                    f"SET name='{name}', note='{note}'" \
                    f"WHERE id='{ id }'"
        db_update(query)

        flash('Changes to feeding type saved!', 'success')
        current_app.logger.info(f"Modified feeding type with id: {id} !")
        return redirect("/settings")
    
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