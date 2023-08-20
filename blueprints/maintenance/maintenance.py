from flask import current_app, render_template, request, redirect, flash, Blueprint
from flask_login import login_required
import os, shutil
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
@login_required
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
    
@maintenance_bp.route("/tasks/<string:task>")
@login_required
def tasks(task):
    print(task)
    if task == 'cleanup_images':
        # Get all animal images
        animal_images = Animal.query.add_columns(Animal.image).all()
        terrarium_images = Terrarium.query.add_columns(Terrarium.image).all()

        for image in os.listdir(f"{UPLOAD_FOLDER}/animals"):
            if str(image) != 'dummy.jpg':
                if any(image in filename for filename in animal_images):
                    print(f"Found {image} in table!")
                else:
                    print(f"Could not find {image} in table!")
                    try:
                        file_path = os.path.join(f"{UPLOAD_FOLDER}/animals", str(image))
                        if os.path.exists(file_path):
                            os.remove(file_path)
                    except:
                        print(f"Could not delete old file: {image}")

        for image in os.listdir(f"{UPLOAD_FOLDER}/terrariums"):
            if str(image) != 'dummy.jpg':
                if any(image in filename for filename in terrarium_images):
                    print(f"Found {image} in table!")
                else:
                    print(f"Could not find {image} in table!")
                    try:
                        file_path = os.path.join(f"{UPLOAD_FOLDER}/terrariums", str(image))
                        if os.path.exists(file_path):
                            os.remove(file_path)
                    except:
                        print(f"Could not delete old file: {image}")


        flash('Deleted old images!', 'success')
        return redirect("/maintenance")
    
    if task == 'color_reset':
        # Color female
        setting = Settings.query.filter(Settings.setting=='color_female').first()
        setting.value='#e481e4'
        db.session.add(setting)
        # Color male
        setting = Settings.query.filter(Settings.setting=='color_male').first()
        setting.value='#89cff0'
        db.session.add(setting)
        # Color other
        setting = Settings.query.filter(Settings.setting=='color_other').first()
        setting.value='#29a039'
        db.session.add(setting)
        db.session.commit()

        flash('Reset colors to default!', 'success')
        return redirect("/maintenance")
    
@maintenance_bp.route("/update")
def do_update():
    print("Running Update...")
    error = ""

    # Rename feeding Table
    exists = False
    exists = db_fetch("SELECT * FROM feeding LIMIT 1")
    if exists:
        try:
            print("DROP auto-generated table feedings")
            query = "DROP TABLE feedings"
            db_update(query)
        except:
            print(f"Error: {e} -> DROP generated table feedings")
            error = error + f"DROP generated table feedings -> Error: {e}\n"

        try:
            print("Rename feeding table to feedings")
            query = "ALTER TABLE feeding RENAME TO feedings"
            db_update(query)
        except:
            print(f"Error: {e} -> Renaming Table")
            error = error + f"Renaming Table feeding to feedings -> Error: {e}\n"

    # Check for feeding size setting
    exists = None
    exists = db_fetch("SELECT * FROM settings WHERE setting='feeding_size'", False)
    if exists == None:
        try:
            print("Insert new setting feeding_size to database")
            type = Settings(setting='feeding_size', value='[\"1\"]', name='Feeding Size', description='Show feeding size for animal type!')
            db.session.add(type)
            db.session.commit()
        except:
            print(f"Error: {e} -> add default feeding_size")
            error = error + f"Could not add default for feeding_size -> Error: {e}\n"

    exists = None
    exists = db_fetch("SELECT * FROM settings WHERE setting='color_female'", False)
    if exists == None:
        try:
            print("Insert new setting gender_colors to database")
            # Color female
            type = Settings(setting='color_female', value='#e481e4', name='Female Color', description='Color for female animals!')
            db.session.add(type)
            # Color male
            type = Settings(setting='color_male', value='#89cff0', name='Male Color', description='Color for male animals!')
            db.session.add(type)
            # Color other
            type = Settings(setting='color_other', value='#29a039', name='Other Color', description='Color for other animals!')
            db.session.add(type)
            db.session.commit()
        except:
            print(f"Error: {e} -> add default colors")
            error = error + f"Could not add default colors -> Error: {e}\n"
    
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

    if not db_col_exists("animals","terrarium"):
        try:
            query= "ALTER TABLE animals ADD terrarium INTEGER"
            db_update(query)
        except Exception as e:
            print(f"Error: {e}")
            error = error + f"Add terrarium to animals -> Error: {e}\n"

    if not db_col_exists("user","is_active"):
        try:
            query= "ALTER TABLE user ADD is_active BOOLEAN DEFAULT 0"
            db_update(query)
            users = User.query.all()
            for user in users:
                user.is_active = 1
                db.session.add(user)
                db.session.commit()
        except Exception as e:
            print(f"Error: {e}")
            error = error + f"Add is_active to user -> Error: {e}\n"

    # Check if a user is admin
    users = User.query.all().count()
    admins = User.query.filter(User.is_admin==True).count()
    if users > 0:
        if admins == 0:
            admin = User.query.first()
            admin.is_admin = True
            db.session.add(admin)
            db.session.commit()
            error = error + f"No admin found! &lt;{admin.email}&gt; is now administrator!"

    # Checking for new defaults
    print("Insert default values")
    try:
        query = f"UPDATE animal_type SET f_min='0', f_max='0' WHERE f_min IS NULL OR f_max IS NULL"
        db_update(query)
    except Exception as e:
        print(f"Error: {e}")
        error = error + f"Add defaults for animal_type -> Error: {e}\n"

    # Migrate images
    print("Migrating images")
    try:
        for image in os.listdir(UPLOAD_FOLDER):
            if allowed_file(image):
                print(f"migrating {image}")
                src = os.path.join(UPLOAD_FOLDER, image)
                dst = os.path.join(f"{UPLOAD_FOLDER}/animals", image)
                shutil.move(src,dst)
    except Exception as e:
        print(f"Error: {e}")
        error = error + f"Migrate animal images to new path -> Error: {e}\n"

    # Done Updating
    if error != "":
        flash(f"<strong>Error while doing update!</strong>\n\n{error}", 'danger')
    else:
        flash("Update done!", 'success')
    return redirect('/')