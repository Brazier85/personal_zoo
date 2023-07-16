import sqlite3
import os

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
    return db_fetch("SELECT id, name, unit, detail FROM feeding_type ORDER BY name ASC")

def get_ht():
    return db_fetch("SELECT id, name, note FROM history_type ORDER BY name ASC")

def get_at():
    return db_fetch("SELECT id, name, f_min, f_max FROM animal_type ORDER BY name ASC")

def get_nf():
    return db_fetch("SELECT id, date, message, interval FROM notifications ORDER BY DATE")

def get_ad(id=None):
    if id:
        animal_data = db_fetch(f"SELECT a.id as id, a.name, at.name as art, a.morph, a.gender, a.birth, a.notes, a.image, a.background_color, a.created_date, a.updated_date, at.id as aid, at.f_min, at.f_max FROM animals a LEFT JOIN animal_type at ON a.art = at.id WHERE a.id={ id }", False)
    else:
        animal_data = db_fetch(f"SELECT a.id as id, a.name, at.name as art, a.morph, a.gender, a.birth, a.notes, a.image, a.background_color, a.created_date, a.updated_date, at.id as aid, at.f_min, at.f_max FROM animals a LEFT JOIN animal_type at ON a.art = at.id ORDER by a.name")
    return animal_data

def get_setting(name=None):
    if (name == None):
        settings = {}
        settings_list = db_fetch("SELECT id, setting, value, name, description FROM settings")
        for setting in settings_list:
            settings.update({setting[1]:[ setting[2], setting[3], setting[4] ]})
        return settings
    else:
        setting = db_fetch(f"SELECT value FROM settings WHERE setting = '{ name }'", False)
        return setting[0]

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
                f"VALUES ('Grasshopper','size','small,middle,sub,adult')"
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
                    unit TEXT,
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
                    unit TEXT,
                    detail TEXT)''')
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
                    f_min INT DEFAULT 0,
                    f_max INT DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS notifications
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date DATE,
                    message TEXT,
                    interval TEXT)''')
    conn.commit()
    conn.close()