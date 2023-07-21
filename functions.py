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

def get_ft():
    return FeedingType.query.all()

def get_ht():
    return HistoryType.query.all()

def get_at():
    return AnimalType.query.all()

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

    notifications = ""

    for notification in notifications:
        print(notification[0])

    #print(f"Found E-Mail config: {EMAIL}, {EMAIL_PASSWORD}, {SMTP_SERVER}, {PORT}")

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
        db.session.commit()


def create_folders():
    if not os.path.exists(UPLOAD_FOLDER):
        print("Create upload folder")
        os.makedirs(UPLOAD_FOLDER)

    if not os.path.exists(f"{UPLOAD_FOLDER}/dummy.jpg"):
        print("Copy dummy image")
        copyfile("static/images/dummy.jpg", f"{UPLOAD_FOLDER}/dummy.jpg")
