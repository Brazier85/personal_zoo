from flask import current_app, render_template, request, redirect, flash, jsonify, Blueprint
from datetime import datetime
from functions import *

document_bp = Blueprint("document", __name__, template_folder="templates")

@document_bp.route('/get_all/<int:id>', methods=['POST','GET'])
def get_all(id):
    if request.method == 'GET':
        less = request.args.get('less')
        if (less):
            feedings=get_fd(None,id,5)
        else:
            feedings=get_fd(None,id)
        return render_template('document_all.html', feedings=feedings)

@document_bp.route('/add/<int:id>', methods=['POST','GET'])
def add(id):
    if request.method == 'GET':
        animal = Animal.query.add_columns(Animal.name, Animal.default_ft).filter(Animal.id==id).one()
        return render_template('document_add.html', id=id, animal=animal, feeding_types=get_ft())
        
    elif request.method == 'POST':
        feeding = request.form
        count = feeding['feeding_count']
        type = feeding['feeding_type']
        unit = feeding['feeding_unit']
        date = feeding['feeding_date']

        date = datetime.datetime.strptime(date, '%Y-%m-%d')
        
        feeding = Feeding(animal=id,
                            type=type,
                            count=count,
                            unit=unit,
                            date=date)
        db.session.add(feeding)
        db.session.commit()

        flash('Added feeding successfully!', 'success')
        current_app.logger.info("Added feeding!")

        return redirect("/animal/"+str(id))   
    
@document_bp.route('/edit/<int:id>', methods=['POST','GET'])
def edit(id):

    feeding = Feeding.query.filter(Feeding.id==id).first()

    if request.method == 'GET':
        return jsonify({'htmlresponse': render_template('document_edit.html', data=feeding, feeding_types=get_ft())})
    
    elif request.method == 'POST':

        feeding_data = request.form
        count = feeding_data['feeding_count']
        type = feeding_data['feeding_type']
        unit = feeding_data['feeding_unit']
        date = feeding_data['feeding_date']
        animal_id = feeding_data['animal_id']

        date = datetime.datetime.strptime(date, '%Y-%m-%d')

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
    
@document_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    if request.method == 'POST': 
        # Delete data into the database
        feeding = Feeding.query.get_or_404(id)
        db.session.delete(feeding)
        db.session.commit()
        flash('Deleted feeding successfully!', 'success')
        current_app.logger.info(f"Deleted feeding with id: {id} !")

        return "", 200