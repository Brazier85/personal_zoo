from flask import current_app, render_template, request, redirect, flash, jsonify, Blueprint
from functions import *

history_bp = Blueprint("history", __name__, template_folder="templates")

@history_bp.route('/get_all/<int:id>', methods=['POST','GET'])
def get_all(id):
    if request.method == 'GET':
        less = request.args.get('less')
        if (less):
            history=get_hd(None,id,5)
        else:
            history=get_hd(None,id)
        return render_template('history_all.html', history=history)
    

@history_bp.route('/add/<int:id>', methods=['POST','GET'])
def add(id):
    if request.method == 'GET':
        return render_template('history_add.html', id=id, event_types=get_ht())

    elif request.method == 'POST':
        history = request.form
        event = history['history_event']
        text = history['history_text']
        date = history['history_date']

        date = datetime.datetime.strptime(date, '%Y-%m-%d')

        event = History(animal=id,
                            event=event,
                            text=text,
                            date=date)
        db.session.add(event)
        db.session.commit()
        
        flash('Added event/action successfully!', 'success')
        current_app.logger.info("Added history!")

        return redirect("/animal/"+str(id))
    
@history_bp.route('/multi', methods=['POST','GET'])
def multi_add():
    if request.method == 'GET':
        terrarium = request.args.get('terrarium')
        animals = Animal.query.add_columns(Animal.id, Animal.name).all()

        if terrarium is None:
            return render_template('history_multi_add.html', animals=animals, event_types=get_ht(), terrariums=get_tr(), location="multi_event")
        else:
            return render_template('history_multi_add.html', animals=animals, event_types=get_ht(), terrariums=get_tr(), t_select=terrarium, location="multi_event")

    elif request.method == 'POST':
        history = request.form
        animals = history.getlist('animals')
        terrariums = history.getlist('terrariums')
        f_event = history['history_event']
        text = history['history_text']
        date = history['history_date']

        date = datetime.datetime.strptime(date, '%Y-%m-%d')

        # Get terrarium animals
        if terrariums != []:
            for terrarium in terrariums:
                additional_animals = Animal.query.filter(Animal.terrarium == terrarium).add_columns(Animal.id).all()
                for animal in additional_animals:
                    if str(animal.id) not in animals:
                        animals.append(f"{animal.id}")

        for animal in animals:
            event = History(animal=animal,
                            event=f_event,
                            text=text,
                            date=date)
            db.session.add(event)
            db.session.commit()
        
        flash('Added event/action successfully!', 'success')
        current_app.logger.info("Added history!")

        return redirect("/")
    
@history_bp.route('/edit/<int:id>', methods=['POST','GET'])
def edit(id):

    event = History.query.filter(History.id==id).first()

    if request.method == 'GET':
        return jsonify({'htmlresponse': render_template('history_edit.html', data=event, event_types=get_ht())})
    
    elif request.method == 'POST':
        history = request.form
        event_type = history['history_event']
        text = history['history_text']
        date = history['history_date']
        animal_id = history['animal_id']

        date = datetime.datetime.strptime(date, '%Y-%m-%d')

        event.animal = animal_id
        event.event = event_type
        event.text = text
        event.date = date
        

        db.session.add(event)
        db.session.commit()

        flash('Changes to history saved!', 'success')
        current_app.logger.info(f"Modified history with id: {id} !")
        return redirect("/animal/"+str(animal_id))

@history_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    if request.method == 'POST': 
        # Delete data into the database
        event = History.query.get_or_404(id)
        db.session.delete(event)
        db.session.commit()

        flash('Deleted history successfully!', 'success')
        current_app.logger.info(f"Deleted history with id: {id} !")

        return "", 200