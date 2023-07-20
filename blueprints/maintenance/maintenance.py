from flask import current_app, render_template, request, redirect, flash, jsonify, Blueprint
from functions import *
import json

maintenance_bp = Blueprint("maintenance", __name__, template_folder="templates")

@maintenance_bp.route("/")
def main():
    location = 'maintenance'
    return render_template('maintenance.html', location=location)

@maintenance_bp.route("/sql", methods=['POST','GET'])
def do_sql():
    if request.method == 'POST':
        data = request.form
        query = data['sqlquery']
        print(query)
        try:
            db_update(query)
        except:
            return "Fehler"
        
        flash('SQL query executed!', 'success')
        current_app.logger.info(f"SQL query executed!")
        return redirect("/maintenance")