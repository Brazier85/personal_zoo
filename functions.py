from datetime import datetime
import sqlite3

# Variables
DATABASE = 'data/database.db'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = str('data/uploads')

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


# Create the DATABASE tables
def create_tables():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # Debug clear feeding table
    # c.execute('''DROP TABLE feeding''')

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
    conn.commit()
    conn.close()