from flask import current_app, render_template, request, redirect, flash, jsonify, Blueprint
from functions import *
import json

settings_bp = Blueprint("settings", __name__, template_folder="templates")

@settings_bp.route("/")
def settings():

    location = 'settings'

    return render_template('settings.html', feeding_types=get_ft(), history_types=get_ht(), ht=get_ht(), settings=get_setting(), animal_types=get_at(), terrarium_types=get_tt(), terrarium_history_types=get_htt(), location=location)

@settings_bp.route('/edit', methods=['POST','GET'])
def edit():
    if request.method == 'GET':
        return 200
    
    elif request.method == 'POST':
        settings = request.form
        weight = settings["weight"]
        feeding_size = settings.getlist('feeding_size')
        color_male = settings["color_male"]
        color_female = settings["color_female"]
        color_other = settings["color_other"]

        print(f"Feeding size: {weight}")

        # Weight setting
        setting = Settings.query.filter(Settings.setting=='weight_type').first()
        setting.value = weight
        db.session.add(setting)
        db.session.commit()

        # Feeding size
        setting = Settings.query.filter(Settings.setting=='feeding_size').first()
        setting.value = json.dumps(feeding_size)
        db.session.add(setting)
        db.session.commit()

        # Color male
        setting = Settings.query.filter(Settings.setting=='color_male').first()
        setting.value = color_male
        db.session.add(setting)
        db.session.commit()

        # Color female
        setting = Settings.query.filter(Settings.setting=='color_female').first()
        setting.value = color_female
        db.session.add(setting)
        db.session.commit()

        # Color other
        setting = Settings.query.filter(Settings.setting=='color_other').first()
        setting.value = color_other
        db.session.add(setting)
        db.session.commit()

        flash('Settings saved!', 'success')
        current_app.logger.info("Settings saved")
        return redirect("/settings")
    

@settings_bp.route('/ft_edit/<int:id>', methods=['POST','GET'])
def ft_edit(id):

    feeding_type = FeedingType.query.filter(FeedingType.id==id).first()

    if request.method == 'GET':
        return jsonify({'htmlresponse': render_template('ft_edit.html', data=feeding_type)})
    
    elif request.method == 'POST':
        data = request.form
        feeding_type.name = data['ft_name']
        feeding_type.unit = data['ft_unit']
        feeding_type.detail = data['ft_detail']

        db.session.add(feeding_type)
        db.session.commit()

        flash('Changes to feeding type saved!', 'success')
        current_app.logger.info(f"Modified feeding type with id: {id} !")
        return redirect("/settings")
    
@settings_bp.route('/ft_add', methods=['POST','GET'])
def ft_add():
    if request.method == 'GET':
        return render_template('ft_add.html')

    elif request.method == 'POST':
        data = request.form
        feeding_type = FeedingType(name=data['ft_name'],
                                unit=data['ft_unit'],
                                detail=data['ft_detail'])
        db.session.add(feeding_type)
        db.session.commit()

        flash('Added feed type successfully!', 'success')
        current_app.logger.info("Added feed type !")

        return redirect("/settings")
    
@settings_bp.route('/ft_delete/<int:id>', methods=['POST'])
def ft_delete(id):
    if request.method == 'POST': 
        # Delete data into the database
        feeding_type = FeedingType.query.get_or_404(id)
        db.session.delete(feeding_type)
        db.session.commit()

        flash('Deleted feeding type successfully!', 'success')
        current_app.logger.info(f"Deleted feeding type with id: {id} !")

        return "", 200
    
@settings_bp.route('/ht_edit/<int:id>', methods=['POST','GET'])
def ht_edit(id):

    history_type = HistoryType.query.filter(HistoryType.id==id).first()

    if request.method == 'GET':
        return jsonify({'htmlresponse': render_template('ht_edit.html', data=history_type)})
    
    elif request.method == 'POST':
        history = request.form
        history_type.name = history['ht_name']
        history_type.note = history['ht_note']

        db.session.add(history_type)
        db.session.commit()

        flash('Changes to history type saved!', 'success')
        current_app.logger.info(f"Modified history type with id: {id} !")
        return redirect("/settings")
    
@settings_bp.route('/ht_add', methods=['POST','GET'])
def ht_add():
    if request.method == 'GET':
        return render_template('ht_add.html')

    elif request.method == 'POST':
        data = request.form
        history_type = HistoryType(name=data['ht_name'],
                                    note=data['ht_note'])
        db.session.add(history_type)
        db.session.commit()
        
        flash('Added history type successfully!', 'success')
        current_app.logger.info("Added history type !")

        return redirect("/settings")
    
@settings_bp.route('/ht_delete/<int:id>', methods=['POST'])
def ht_delete(id):
    if request.method == 'POST': 
        # Delete data into the database
        history_type = HistoryType.query.get_or_404(id)
        db.session.delete(history_type)
        db.session.commit()

        flash('Deleted history type successfully!', 'success')
        current_app.logger.info(f"Deleted history type with id: {id} !")

        return "", 200
    
@settings_bp.route('/at_edit/<int:id>', methods=['POST','GET'])
def at_edit(id):

    animal_type = AnimalType.query.filter(AnimalType.id==id).first()

    if request.method == 'GET':
        return jsonify({'htmlresponse': render_template('at_edit.html', data=animal_type)})
    
    elif request.method == 'POST':
        data = request.form
        animal_type.name = data['at_name']
        animal_type.f_min = data['at_f_min']
        animal_type.f_max = data['at_f_max']

        db.session.add(animal_type)
        db.session.commit()

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

        if f_min == "":
            f_min = 0

        if f_max == "":
            f_max = 0 

        animal_type = AnimalType(name=name,
                                f_min=f_min,
                                f_max=f_max)
        db.session.add(animal_type)
        db.session.commit()

        flash('Added animal type successfully!', 'success')
        current_app.logger.info("Added animal type !")

        return redirect("/settings")
    
@settings_bp.route('/at_delete/<int:id>', methods=['POST'])
def at_delete(id):
    if request.method == 'POST': 
        # Delete data into the database
        animal_type = AnimalType.query.get_or_404(id)
        db.session.delete(animal_type)
        db.session.commit()

        flash('Deleted animal type successfully!', 'success')
        current_app.logger.info(f"Deleted animal type with id: {id} !")

        return "", 200
    
@settings_bp.route('/tt_edit/<int:id>', methods=['POST','GET'])
def tt_edit(id):

    terrarium_type = TerrariumType.query.filter(TerrariumType.id==id).first()

    if request.method == 'GET':
        return jsonify({'htmlresponse': render_template('tt_edit.html', data=terrarium_type)})
    
    elif request.method == 'POST':
        data = request.form
        terrarium_type.name = data['tt_name']

        db.session.add(terrarium_type)
        db.session.commit()

        flash('Changes to terrarium type saved!', 'success')
        current_app.logger.info(f"Modified terrarium type with id: {id} !")
        return redirect("/settings")
    
@settings_bp.route('/tt_add', methods=['POST','GET'])
def tt_add():
    if request.method == 'GET':
        return render_template('tt_add.html')

    elif request.method == 'POST':
        data = request.form
        terrarium_type = TerrariumType(name=data['tt_name'])
        db.session.add(terrarium_type)
        db.session.commit()
        
        flash('Added terrarium type successfully!', 'success')
        current_app.logger.info("Added terrarium type !")

        return redirect("/settings")
    
@settings_bp.route('/tt_delete/<int:id>', methods=['POST'])
def tt_delete(id):
    if request.method == 'POST': 
        # Delete data into the database
        terrarium_type = TerrariumType.query.get_or_404(id)
        db.session.delete(terrarium_type)
        db.session.commit()

        flash('Deleted terrarium type successfully!', 'success')
        current_app.logger.info(f"Deleted terrarium type with id: {id} !")

        return "", 200
    
@settings_bp.route('/htt_edit/<int:id>', methods=['POST','GET'])
def htt_edit(id):

    history_type = TerrariumHistoryType.query.filter(TerrariumHistoryType.id==id).first()

    if request.method == 'GET':
        return jsonify({'htmlresponse': render_template('htt_edit.html', data=history_type)})
    
    elif request.method == 'POST':
        history = request.form
        history_type.name = history['htt_name']
        history_type.note = history['htt_note']

        db.session.add(history_type)
        db.session.commit()

        flash('Changes to terrarium history type saved!', 'success')
        current_app.logger.info(f"Modified terrarium history type with id: {id} !")
        return redirect("/settings")
    
@settings_bp.route('/htt_add', methods=['POST','GET'])
def htt_add():
    if request.method == 'GET':
        return render_template('htt_add.html')

    elif request.method == 'POST':
        data = request.form
        history_type = TerrariumHistoryType(name=data['htt_name'],
                                    note=data['htt_note'])
        db.session.add(history_type)
        db.session.commit()
        
        flash('Added terrarium history type successfully!', 'success')
        current_app.logger.info("Added terrarium history type !")

        return redirect("/settings")
    
@settings_bp.route('/htt_delete/<int:id>', methods=['POST'])
def htt_delete(id):
    if request.method == 'POST': 
        # Delete data into the database
        history_type = TerrariumHistoryType.query.get_or_404(id)
        db.session.delete(history_type)
        db.session.commit()

        flash('Deleted terrarium history type successfully!', 'success')
        current_app.logger.info(f"Deleted terrarium history type with id: {id} !")

        return "", 200