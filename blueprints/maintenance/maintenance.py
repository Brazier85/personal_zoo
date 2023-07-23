from flask import current_app, render_template, request, redirect, flash, Blueprint
from functions import *

maintenance_bp = Blueprint("maintenance", __name__, template_folder="templates")

def db_fetch(query, mode = True):
    try:
        conn = sqlite3.connect(current_app.config.get('DATABASE'))
        
        c = conn.cursor()
        c.execute(query)

        # Fetch all
        if (mode):
            data = c.fetchall()
        else:
            data = c.fetchone()

        # Close connection
        conn.close()

        return data
    except:
        return False

def db_update(query):
    try:
        conn = sqlite3.connect(current_app.config.get('DATABASE'))
        c = conn.cursor()
        c.execute(query)
        conn.commit()
        conn.close()
        return True
    except:
        return False

def db_col_exists(table, col):
    try:
        result = db_fetch(f"SELECT COUNT(*) AS column_exists FROM pragma_table_info('{table}') WHERE name='{col}'", False)[0]
        if result > 0:
            return True
        else:
            return False
    except:
        return False
    

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
            conn = sqlite3.connect(DATABASE)
            c = conn.cursor()
            c.execute(query)
            conn.commit()
            conn.close()
        except:
            return "Fehler"
        
        flash('SQL query executed!', 'success')
        current_app.logger.info(f"SQL query executed!")
        return redirect("/maintenance")
    
@maintenance_bp.route("/update")
def do_update():
    print("Running Update...")
    error = ""

    # Check for feeding size setting
    exists = None
    exists = db_fetch("SELECT * FROM settings WHERE setting='feeding_size'", False)
    if exists == None:
        print("Insert new setting feeding_size to database")
        query = "INSERT INTO settings " \
                "(setting, value, name, description)" \
                f"VALUES ('feeding_size','[\"1\"]','Feeding Size','Show feeding size for animal type!')"
        db_update(query)
    
    ## Delete old cols
    print("Remove old columns....")
    if db_col_exists("animal_type","note"):
        try:
            query= "ALTER TABLE animal_type DROP COLUMN note"
            db_update(query)
        except Exception as e:
            print(f"Error: {e} -> Remove old column")
            error = error + f"Remove old column 'note' from animal_type -> Error: {e}\n"

    if db_col_exists("feeding_type","note"):
        try:
            query= "ALTER TABLE feeding_type DROP COLUMN note"
            db_update(query)
        except Exception as e:
            print(f"Error: {e} -> Remove old column")
            error = error + f"Remove old column 'note' from feeding_type -> Error: {e}\n"

    # Add new cols
    print("Add new columns")
    if not db_col_exists("animals","default_ft"):
        try:
            query= "ALTER TABLE animals ADD default_ft INTEGER"
            db_update(query)
        except Exception as e:
            print(f"Error: {e}")
            error = error + f"Add default_ft to animals -> Error: {e}\n"

    # Checking for new defaults
    print("Insert default values")
    try:
        query = f"UPDATE animal_type SET f_min='0', f_max='0' WHERE f_min IS NULL OR f_max IS NULL"
        db_update(query)
    except Exception as e:
        print(f"Error: {e}")
        error = error + f"Add defaults for animal_type -> Error: {e}\n"

    # Done Updateing
    if error != "":
        flash(f"<strong>Error while doing update!</strong>\n\n{error}", 'danger')
    else:
        flash("Update done!", 'success')
    return redirect('/')