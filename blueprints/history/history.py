from flask import current_app, render_template, request, redirect, flash, jsonify, url_for, Blueprint
from flask_login import login_required
from functions import *

from .forms import HistoryForm, HistoryMultiForm

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
@login_required
def add(id):

    form = HistoryForm(request.form)

    # Adding select values
    form.event.choices = [(i.id, i.name) for i in get_ht()]

    if form.validate_on_submit():
        event = form.event.data
        text = form.text.data
        date = form.date.data

        event = History(animal=id,
                            event=event,
                            text=text,
                            date=date)
        db.session.add(event)
        db.session.commit()
        
        flash('Added event/action successfully!', 'success')
        current_app.logger.info("Added history!")

        return jsonify(status='ok')
    elif request.method == 'GET':
        return render_template('history_add.html', id=id, form=form, target=url_for('history.add', id=id))
    else:
        data = json.dumps(form.errors, ensure_ascii=False)
        return jsonify(data)
    
@history_bp.route('/multi', methods=['POST','GET'])
@login_required
def multi_add():

    terrarium = request.args.get('terrarium')

    form = HistoryMultiForm(request.form)

    # Adding select values
    form.event.choices = [(i.id, i.name) for i in get_ht()]
    form.animals.choices = [(i.id, i.name) for i in Animal.query.add_columns(Animal.id, Animal.name).all()]
    form.terrariums.choices = [(i["id"], i["name"]) for i in get_tr()]

    if form.validate_on_submit():
        animals = form.animals.data
        terrariums = form.terrariums.data
        f_event = form.event.data
        text = form.text.data
        date = form.date.data

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

        return jsonify(status='ok')
    elif request.method == 'GET':
        terrarium = request.args.get('terrarium')
        animals = Animal.query.add_columns(Animal.id, Animal.name).all()

        if terrarium is None:
            return render_template('history_multi_add.html', form=form, location="multi_event")
        else:
            return render_template('history_multi_add.html', form=form, terrarium=terrarium, location="multi_event")
    else:
        data = json.dumps(form.errors, ensure_ascii=False)
        return jsonify(data)
    
@history_bp.route('/edit/<int:id>', methods=['POST','GET'])
@login_required
def edit(id):

    f_event = History.query.filter(History.id==id).first()

    form = HistoryForm(request.form, obj=f_event)

    # Adding select values
    form.event.choices = [(i.id, i.name) for i in get_ht()]

    if form.validate_on_submit():
        f_event.event = form.event.data
        f_event.text = form.text.data
        f_event.date = form.date.data
        
        db.session.add(f_event)
        db.session.commit()

        flash('Changes to history saved!', 'success')
        current_app.logger.info(f"Modified history with id: {id} !")
        return jsonify(status='ok')
    elif request.method == 'GET':
        return jsonify({'htmlresponse': render_template('history_edit.html', form=form, target=url_for("history.edit", id=id), id=id)})
    else:
        data = json.dumps(form.errors, ensure_ascii=False)
        return jsonify(data)

@history_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    if request.method == 'POST': 
        # Delete data into the database
        event = History.query.get_or_404(id)
        db.session.delete(event)
        db.session.commit()

        flash('Deleted history successfully!', 'success')
        current_app.logger.info(f"Deleted history with id: {id} !")

        return "", 200