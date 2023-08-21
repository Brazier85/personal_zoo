import sqlite3
import os
from shutil import copyfile
from models import *

# Variables
DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/database.db')
UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

# Check if a file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Get feeding types
def get_ft():
    return FeedingType.query.all()

# Get history types
def get_ht():
    return HistoryType.query.all()

# get terrarium history types
def get_htt():
    return TerrariumHistoryType.query.all()

# Get animal types
def get_at():
    return AnimalType.query.all()

# Get animal history data
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

# Get terrarium history data
def get_thd(id=None, terrarium_id=None, limit=None):
    if id:
        event_with_type = db.session.query(TerrariumHistory, TerrariumHistoryType).join(TerrariumHistoryType, TerrariumHistoryType.id == TerrariumHistory.event).filter(TerrariumHistory.terrarium == terrarium_id).first()
        vEvent= event_with_type[0]
        vEventType = event_with_type[1]
        event = {
            'id': vEvent.id,
            'terrarium': vEvent.terrarium,
            'name': vEventType.name,
            'text': vEvent.text,
            'date': vEvent.date
        }
        return event
    else:
        events_with_type = db.session.query(TerrariumHistory, TerrariumHistoryType).join(TerrariumHistoryType, TerrariumHistoryType.id == TerrariumHistory.event).filter(TerrariumHistory.terrarium == terrarium_id).order_by(TerrariumHistory.date.desc()).limit(limit).all()   
        events = []
        for vEvent, vEventType in events_with_type:
            events.append({
                'id': vEvent.id,
                'terrarium': vEvent.terrarium,
                'name': vEventType.name,
                'text': vEvent.text,
                'date': vEvent.date
            })
        return events

# Get feeding data
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

# Get animal data
def get_ad(id=None, terrarium=None):
    if id:
        animal_with_type = db.session.query(Animal, AnimalType).join(AnimalType, AnimalType.id == Animal.art).filter(Animal.id==id).first()
        vAnimal = animal_with_type[0]
        vAnimalType = animal_with_type[1]
        animal = {
            'id': vAnimal.id,
            'name': vAnimal.name,
            'art': vAnimalType.name,
            'art_id': vAnimalType.id,
            'morph': vAnimal.morph,
            'gender': vAnimal.gender,
            'birth': vAnimal.birth,
            'notes': vAnimal.notes,
            'image': vAnimal.image,
            'background_color': vAnimal.background_color,
            'f_min': vAnimalType.f_min,
            'f_max': vAnimalType.f_max,
            'default_ft': vAnimal.default_ft,
            'terrarium': vAnimal.terrarium,
            'updated_date': vAnimal.updated_date
        }
        return animal
    elif terrarium:
        animals_with_type = db.session.query(Animal, AnimalType).join(AnimalType, AnimalType.id == Animal.art).filter(Animal.terrarium==terrarium).all()   
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
                'default_ft': vAnimal.default_ft,
                'terrarium': vAnimal.terrarium,
                'updated_date': vAnimal.updated_date
            })
        return animals
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
                'default_ft': vAnimal.default_ft,
                'terrarium': vAnimal.terrarium,
                'updated_date': vAnimal.updated_date
            })
        return animals

# Get terrarium types
def get_tt():
    return TerrariumType.query.all()

# Get terrarium equipment
def get_te(id=None, terrarium_id=None):
    if id:
        return TerrariumEquipment.query.filter(TerrariumEquipment.terrarium == terrarium_id).first()
    else:
        return TerrariumEquipment.query.filter(TerrariumEquipment.terrarium == terrarium_id).order_by(TerrariumEquipment.name.asc()).order_by(TerrariumEquipment.text.asc()).all()

# Get terrarium lamps    
def get_tl(id=None, terrarium_id=None):
    if id:
        return TerrariumLamps.query.filter(TerrariumLamps.terrarium == terrarium_id).first()
    else:
        return TerrariumLamps.query.filter(TerrariumLamps.terrarium == terrarium_id).order_by(TerrariumLamps.type.asc()).order_by(TerrariumLamps.watt.asc()).all() 

# Get terrarium data
def get_tr(id=None):
    if id:
        terrarium_with_type = db.session.query(Terrarium, TerrariumType).join(TerrariumType, TerrariumType.id == Terrarium.type).filter(Terrarium.id==id).first()
        vTerrarium = terrarium_with_type[0]
        vTerrariumType = terrarium_with_type[1]
        terrarium = {
            'id': vTerrarium.id,
            'name': vTerrarium.name,
            'size': vTerrarium.size,
            'type_id': vTerrariumType.id,
            'type': vTerrariumType.name,
            'notes': vTerrarium.notes,
            'image': vTerrarium.image
        }
        return terrarium
    else:
        terrariums_with_type = db.session.query(Terrarium, TerrariumType).join(TerrariumType, TerrariumType.id == Terrarium.type).all()   
        terrariums = []
        for vTerrarium, vTerrariumType in terrariums_with_type:
            terrariums.append({
                'id': vTerrarium.id,
                'name': vTerrarium.name,
                'size': vTerrarium.size,
                'type_id': vTerrariumType.id,
                'type': vTerrariumType.name,
                'notes': vTerrarium.notes,
                'image': vTerrarium.image
            })
        return terrariums

# Get documents
def get_docs(target, id):
    if target == 'animal':
        return Document.query.filter(Document.animal_id==id).all()
    elif target == 'terrarium':
        return Document.query.filter(Document.terrarium_id==id).all()
            

# get setting values
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

# Send a mail
# Alpha function - not working
def send_mail():
    EMAIL = os.getenv("PZOO_EMAIL")
    EMAIL_PASSWORD = os.getenv("PZOO_EMAIL_PASSWORD")
    SMTP_SERVER = os.getenv("PZOO_SMTP_SERVER")
    PORT = os.getenv("PZOO_SMTP_PORT")

    notifications = ""

    for notification in notifications:
        print(notification[0])

    #print(f"Found E-Mail config: {EMAIL}, {EMAIL_PASSWORD}, {SMTP_SERVER}, {PORT}")

# Insert database defaults
def insert_defaults():

    # Add animal defaults
    animal_types = AnimalType.query.all()
    if animal_types == []:
        # Insert base data
        type = AnimalType(name='Ball Python', f_min=10, f_max=20)
        db.session.add(type)
        type = AnimalType(name='Leopard Gecko', f_min=0, f_max=0)
        db.session.add(type)
        db.session.commit()

    # Add feeding defaults
    feeding_types = FeedingType.query.all()
    if feeding_types == []:
        # Insert base data
        type = FeedingType(name='Elephant', unit='weight', detail='t')
        db.session.add(type)
        type = FeedingType(name='Toddler', unit='text', detail='BMI')
        db.session.add(type)
        type = FeedingType(name='Mouse', unit='weight', detail='gr')
        db.session.add(type)
        type = FeedingType(name='Rat', unit='weight', detail='gr')
        db.session.add(type)
        type = FeedingType(name='Whale', unit='weight', detail='t')
        db.session.add(type)
        type = FeedingType(name='Grasshopper', unit='size', detail='small,medium,sub,adult')
        db.session.add(type)
        db.session.commit()
    
    # Add history defaults
    history_types = HistoryType.query.all()
    if history_types == []:
        # Insert base data
        EVENT_TYPES =  ["Shed","Weighed","Medical","Miscellaneous"]
        for e_type in EVENT_TYPES:
            type = HistoryType(name=e_type)
            db.session.add(type)
            db.session.commit()

    # Default general settings
    settings = Settings.query.all()
    if settings == []:
        # Weight
        type = Settings(setting='weight_type', value='2', name='Weight Option', description='Last entry will be shown as weight on the animal page!')
        db.session.add(type)
        # Feeding size
        type = Settings(setting='feeding_size', value='[\"1\"]', name='Feeding Size', description='Show feeding size for animal type!')
        db.session.add(type)
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

    # Add terrarium defaults
    terrarium_types = TerrariumType.query.all()
    if terrarium_types == []:
        # Insert base data
        type = TerrariumType(name='Tropical')
        db.session.add(type)
        type = TerrariumType(name='Desert')
        db.session.add(type)
        db.session.commit()

    # Add terrarium event defaults
    terrarium_history_types = TerrariumHistoryType.query.all()
    if terrarium_history_types == []:
        # Insert base data
        T_EVENT_TYPES =  ["Cleaning","Maintenance"]
        for e_type in T_EVENT_TYPES:
            type = TerrariumHistoryType(name=e_type)
            db.session.add(type)
            db.session.commit()

# Create required folders and files
def create_folders(name=None):
    if not os.path.exists(UPLOAD_FOLDER):
        print("Create upload folder")
        os.makedirs(UPLOAD_FOLDER)

    if not os.path.exists(f"{UPLOAD_FOLDER}/terrariums"):
        print("Create terrarium upload folder")
        os.makedirs(f"{UPLOAD_FOLDER}/terrariums")

    if not os.path.exists(f"{UPLOAD_FOLDER}/animals"):
        print("Create animal upload folder")
        os.makedirs(f"{UPLOAD_FOLDER}/animals")

    if not os.path.exists(f"{UPLOAD_FOLDER}/documents"):
        print("Create document upload folder")
        os.makedirs(f"{UPLOAD_FOLDER}/documents")

    if not os.path.exists(f"{UPLOAD_FOLDER}/animals/dummy.jpg"):
        print("Copy dummy image")
        copyfile("static/images/dummy.jpg", f"{UPLOAD_FOLDER}/animals/dummy.jpg")

    if not os.path.exists(f"{UPLOAD_FOLDER}/terrariums/dummy.jpg"):
        print("Copy dummy image")
        copyfile("static/images/dummy_big.jpg", f"{UPLOAD_FOLDER}/terrariums/dummy.jpg")

# Add col to table
def add_col(table, col, type):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    exists = None
    exists = c.execute(f"SELECT COUNT(*) AS column_exists FROM pragma_table_info('{table}') WHERE name='{col}'")
    print(f"Exist: {exists}")
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute(query)
        conn.commit()
        conn.close()
    except:
        print("Error creating col")

