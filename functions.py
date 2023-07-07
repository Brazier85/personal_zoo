from flask import current_app
from datetime import datetime
import sqlite3
import os

# Variables
DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/database.db')
UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Check if a file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Formate date
def date_eu(dates, row_number):
    if type(dates) is tuple:
        try:
            data_list = list(dates)
            data_list[row_number] = datetime.strptime(dates[row_number], '%Y-%m-%d').strftime('%d.%m.%Y')
            formatted_dates= tuple(data_list)
            return formatted_dates
        except Exception as error:
            return dates
    else:
        try:
            formatted_dates = []
            for row in dates:
                formatted_row = list(row)
                formatted_row[row_number] = datetime.strptime(formatted_row[row_number], '%Y-%m-%d').strftime('%d.%m.%Y')
                formatted_dates.append(formatted_row)
            return formatted_dates
        except Exception as error:
            return dates
        

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

def get_ft():
    return db_fetch("SELECT id, name, note FROM feeding_type ORDER BY name ASC")

def get_ht():
    return db_fetch("SELECT id, name, note FROM history_type ORDER BY name ASC")

def get_at():
    return db_fetch("SELECT id, name, note FROM animal_type ORDER BY name ASC")

def get_setting(name=None):
    if (name == None):
        settings = {}
        settings_list = db_fetch("SELECT id, setting, value, name, description FROM settings")
        print(settings_list)
        for setting in settings_list:
            settings.update({setting[1]:[ setting[2], setting[3], setting[4] ]})
        return settings
    else:
        setting = db_fetch(f"SELECT value FROM settings WHERE setting = '{ name }'", False)
        return setting[0]

def insert_defaults():

     # Add animal defaults
    animal_types = db_fetch("SELECT * FROM animal_type ORDER BY name DESC")
    print(f"Types: {animal_types}")
    if animal_types == []:
        # Insert base data
        ANIMAL_TYPES =  ["Ball Python","Leopard Gecko"]
        for type in ANIMAL_TYPES:
            query = "INSERT INTO animal_type " \
                    "(name)" \
                    f"VALUES ('{type}')"
            db_update(query)

    # Add feeding defaults
    feeding_types = db_fetch("SELECT * FROM feeding_type ORDER BY name DESC")
    if feeding_types == []:
        # Insert base data
        FEEDING_TYPES =  ["Elephant","Toddler","Mouse","Rat","Whale"]
        for type in FEEDING_TYPES:
            query = "INSERT INTO feeding_type " \
                    "(name)" \
                    f"VALUES ('{type}')"
            db_update(query)
    
    # Add history defaults
    history_types = db_fetch("SELECT * FROM history_type ORDER BY name DESC")
    print(f"Types: {history_types}")
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
    print(f"Types: {settings}")
    if settings == []:
        # Weight
        query = "INSERT INTO settings " \
                    "(setting, value, name, description)" \
                    f"VALUES ('weight_type','2','Weight Option','Last entry will be shown as weight on the animal page!')"
        db_update(query)

    #Migration stuff
    #query = "UPDATE animals SET art='1' WHERE art='Königspython'"
    #db_update(query)

    #query = "UPDATE animals SET art='2' WHERE art='Leopardgecko'"
    #db_update(query)


# Create the DATABASE tables
def create_tables():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # Debug clear feeding table
    # c.execute('''DROP TABLE settings''')

    # Create animal table
    c.execute('''CREATE TABLE IF NOT EXISTS animals
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    art TEXT,
                    morph TEXT,
                    gender TEXT,
                    birth DATE,
                    notes TEXT,
                    image TEXT,
                    background_color TEXT,
                    created_date DATE DEFAULT CURRENT_DATE,
                    updated_date DATE DEFAULT CURRENT_DATE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS feeding
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    animal INT,
                    type TEXT,
                    count INT,
                    weight INT,
                    date DATE DEFAULT CURRENT_DATE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS history
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    animal INT,
                    event TEXT,
                    text TEXT,
                    date DATE DEFAULT CURRENT_DATE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS feeding_type
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    note TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS history_type
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    note TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS settings
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    setting TEXT,
                    value TEXT,
                    name TEXT, 
                    description TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS animal_type
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    note TEXT)''')
    conn.commit()
    conn.close()