import sqlite3
import os
from shutil import copyfile
from models import *

# Variables
DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/database.db')
UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Check if a file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def db_fetch(query, mode = True):
    conn = sqlite3.connect(DATABASE)
    
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

def db_update(query):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute(query)
    conn.commit()
    conn.close()

def db_col_exists(table, col):
    try:
        result = db_fetch(f"SELECT COUNT(*) AS column_exists FROM pragma_table_info('{table}') WHERE name='{col}'", False)[0]
        if result > 0:
            return True
        else:
            return False
    except:
        return False

def get_ft():
    return FeedingType.query.all()

def get_ht():
    return HistoryType.query.all()

def get_at():
    return AnimalType.query.all()

def get_nf():
    return db_fetch("SELECT id, date, message, interval FROM notifications ORDER BY DATE")

def get_hd(id=None, animal_id=None, limit=None):
    if id:
        event_with_type = db.session.query(History, HistoryType).join(HistoryType, HistoryType.id == History.event).filter(History.animal == animal_id).first()
        vEvent= event_with_type[0]
        vEventType = event_with_type[1]
        event = {
            'id': vEvent.id,
            'animal': vEvent.animal,
            'name': vEventType.name,
            'text': vEvent.text,
            'date': vEvent.date
        }
        return event
    else:
        events_with_type = db.session.query(History, HistoryType).join(HistoryType, HistoryType.id == History.event).filter(History.animal == animal_id).order_by(History.date.desc()).limit(limit).all()   
        events = []
        for vEvent, vEventType in events_with_type:
            events.append({
                'id': vEvent.id,
                'animal': vEvent.animal,
                'name': vEventType.name,
                'text': vEvent.text,
                'date': vEvent.date
            })
        return events

def get_fd(id=None, animal_id=None, limit=None):
    if id:
        feeding_with_type = db.session.query(Feeding, FeedingType).join(FeedingType, FeedingType.id == Feeding.type).filter(Feeding.id==id).first()
        vFeeding = feeding_with_type[0]
        vFeedingType = feeding_with_type[1]
        feeding = {
            'id': vFeeding.id,
            'animal': vFeeding.animal,
            'type': vFeedingType.name,
            'ftunit': vFeedingType.unit,
            'detail': vFeedingType.detail,
            'count': vFeeding.count,
            'unit': vFeeding.unit,
            'date': vFeeding.date
        }
        return feeding
    else:
        feedings_with_type = db.session.query(Feeding, FeedingType).join(FeedingType, FeedingType.id == Feeding.type).filter(Feeding.animal == animal_id).order_by(Feeding.date.desc()).limit(limit).all()   
        feedings = []
        for vFeeding, vFeedingType in feedings_with_type:
            feedings.append({
                'id': vFeeding.id,
                'animal': vFeeding.animal,
                'type': vFeedingType.name,
                'ftunit': vFeedingType.unit,
                'detail': vFeedingType.detail,
                'count': vFeeding.count,
                'unit': vFeeding.unit,
                'date': vFeeding.date
            })
        return feedings

def get_ad(id=None):
    if id:
        animal_with_type = db.session.query(Animal, AnimalType).join(AnimalType, AnimalType.id == Animal.art).filter(Animal.id==id).first()
        vAnimal = animal_with_type[0]
        vAnimalType = animal_with_type[1]
        animal = {
            'id': vAnimal.id,
            'name': vAnimal.name,
            'art': vAnimalType.name,
            'morph': vAnimal.morph,
            'gender': vAnimal.gender,
            'birth': vAnimal.birth,
            'notes': vAnimal.notes,
            'image': vAnimal.image,
            'background_color': vAnimal.background_color,
            'f_min': vAnimalType.f_min,
            'f_max': vAnimalType.f_max,
            'updated_date': vAnimal.updated_date
        }
        return animal
    else:
        animals_with_type = db.session.query(Animal, AnimalType).join(AnimalType, AnimalType.id == Animal.art).all()   
        animals = []
        for vAnimal, vAnimalType in animals_with_type:
            animals.append({
                'id': vAnimal.id,
                'name': vAnimal.name,
                'art': vAnimalType.name,
                'morph': vAnimal.morph,
                'gender': vAnimal.gender,
                'birth': vAnimal.birth,
                'notes': vAnimal.notes,
                'image': vAnimal.image,
                'background_color': vAnimal.background_color,
                'f_min': vAnimalType.f_min,
                'f_max': vAnimalType.f_max,
                'updated_date': vAnimal.updated_date
            })
        print(animals)
        return animals

def get_setting(name=None):
    if (name == None):
        settings = {}
        settings_list = Settings.query.add_columns(Settings.id, Settings.setting, Settings.value, Settings.name, Settings.description).all()
        for setting in settings_list:
            settings.update({setting.setting:[ setting.value, setting.name, setting.description ]})
        return settings
    else:
        setting = Settings.query.filter(Settings.setting==name).add_columns(Settings.value).first()
        return setting.value

def send_mail():
    EMAIL = os.getenv("PZOO_EMAIL")
    EMAIL_PASSWORD = os.getenv("PZOO_EMAIL_PASSWORD")
    SMTP_SERVER = os.getenv("PZOO_SMTP_SERVER")
    PORT = os.getenv("PZOO_SMTP_PORT")

    notifications = get_nf()

    for notification in notifications:
        print(notification[0])

    #print(f"Found E-Mail config: {EMAIL}, {EMAIL_PASSWORD}, {SMTP_SERVER}, {PORT}")

def insert_defaults():

    # Add animal defaults
    animal_types = db_fetch("SELECT * FROM animal_type ORDER BY name DESC")
    if animal_types == []:
        # Insert base data
        query = "INSERT INTO animal_type " \
                "(name, f_min, f_max)" \
                f"VALUES ('Ball Python', '10', '20')"
        db_update(query)
        query = "INSERT INTO animal_type " \
                "(name, f_min, f_max)" \
                f"VALUES ('Leopard Gecko', '0', '0')"
        db_update(query)

    # Add feeding defaults
    feeding_types = db_fetch("SELECT * FROM feeding_type ORDER BY name DESC")
    if feeding_types == []:
        # Insert base data
        query = "INSERT INTO feeding_type " \
                "(name, unit, detail)" \
                f"VALUES ('Elephant','weight','t')"
        db_update(query)
        query = "INSERT INTO feeding_type " \
                "(name, unit, detail)" \
                f"VALUES ('Toddler','text','BMI')"
        db_update(query)
        query = "INSERT INTO feeding_type " \
                "(name, unit, detail)" \
                f"VALUES ('Mouse','weight','gr')"
        db_update(query)
        query = "INSERT INTO feeding_type " \
                "(name, unit, detail)" \
                f"VALUES ('Rat','weight','gr')"
        db_update(query)
        query = "INSERT INTO feeding_type " \
                "(name, unit, detail)" \
                f"VALUES ('Whale','weight','t')"
        db_update(query)
        query = "INSERT INTO feeding_type " \
                "(name, unit, detail)" \
                f"VALUES ('Grasshopper','size','small,medium,sub,adult')"
        db_update(query)
    
    # Add history defaults
    history_types = db_fetch("SELECT * FROM history_type ORDER BY name DESC")
    if history_types == []:
        # Insert base data
        EVENT_TYPES =  ["Shed","Weighed","Medical","Miscellaneous"]
        for type in EVENT_TYPES:
            query = "INSERT INTO history_type " \
                    "(name)" \
                    f"VALUES ('{type}')"
            db_update(query)

    # Default general settings
    settings = db_fetch("SELECT * FROM settings DESC")
    if settings == []:
        # Weight
        query = "INSERT INTO settings " \
                    "(setting, value, name, description)" \
                    f"VALUES ('weight_type','2','Weight Option','Last entry will be shown as weight on the animal page!')"
        db_update(query)
        query = "INSERT INTO settings " \
                    "(setting, value, name, description)" \
                    f"VALUES ('feeding_size','[\"1\"]','Feeding Size','Show feeding size for animal type!')"
        db_update(query)

def create_folders():
    if not os.path.exists(UPLOAD_FOLDER):
        print("Create upload folder")
        os.makedirs(UPLOAD_FOLDER)

    if not os.path.exists(f"{UPLOAD_FOLDER}/dummy.jpg"):
        print("Copy dummy image")
        copyfile("static/images/dummy.jpg", f"{UPLOAD_FOLDER}/dummy.jpg")
