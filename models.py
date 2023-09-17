from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash
import datetime

db = SQLAlchemy()

class AnimalType(db.Model):
    __tablename__ = 'animal_type'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    f_min = db.Column(db.Integer, default=0)
    f_max = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<AnimalType %r>' % self.name

class FeedingType(db.Model):
    __tablename__ = 'feeding_type'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    unit = db.Column(db.String)
    detail = db.Column(db.String)

class HistoryType(db.Model):
    __tablename__ = 'history_type'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    note = db.Column(db.String)

class Animal(db.Model):
    __tablename__ = 'animals'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    art = db.db.Column(db.Integer)
    morph = db.Column(db.String)
    gender = db.Column(db.String)
    birth = db.Column(db.String)
    notes = db.Column(db.String)
    image = db.Column(db.String)
    default_ft = db.Column(db.Integer)
    terrarium = db.Column(db.Integer)
    background_color = db.Column(db.String)
    created_date = db.Column(db.Date, default=datetime.datetime.utcnow)
    updated_date = db.Column(db.Date, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Animal %r>' % self.name

class Feeding(db.Model):
    __tablename__ = 'feedings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    animal = db.Column(db.Integer)
    type = db.Column(db.Integer)
    count = db.Column(db.Integer)
    unit = db.Column(db.String)
    date = db.Column(db.Date, default=datetime.datetime.utcnow)

class History(db.Model):
    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    animal = db.Column(db.Integer)
    event = db.Column(db.String)
    text = db.Column(db.String)
    date = db.Column(db.Date, default=datetime.datetime.utcnow)

class Settings(db.Model):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    setting = db.Column(db.String)
    value = db.Column(db.String)
    name = db.Column(db.String)
    description = db.Column(db.String)

class Notifications(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date)
    message = db.Column(db.String)
    interval = db.Column(db.String)

class Terrarium(db.Model):
    __tablename__ = 'terrariums'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    size = db.Column(db.String)
    type = db.Column(db.Integer)
    notes = db.Column(db.Text)
    image = db.Column(db.String)

class TerrariumType(db.Model):
    __tablename__ = 'terrarium_type'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)

class TerrariumEquipment(db.Model):
    __tablename__ = 'terrarium_equipment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    terrarium = db.Column(db.Integer)
    name = db.Column(db.String)
    text = db.Column(db.Text)

class TerrariumLamps(db.Model):
    __tablename__ = 'terrarium_lamps'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    terrarium = db.Column(db.Integer)
    type = db.Column(db.String)
    watt = db.Column(db.Text)
    position = db.Column(db.String)
    changed = db.Column(db.Date)

class TerrariumHistory(db.Model):
    __tablename__ = 'terrarium_history'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    terrarium = db.Column(db.Integer)
    event = db.Column(db.String)
    text = db.Column(db.String)
    date = db.Column(db.Date, default=datetime.datetime.utcnow)

class TerrariumHistoryType(db.Model):
    __tablename__ = 'terrarium_history_type'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    note = db.Column(db.String)

class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    filename = db.Column(db.String, nullable=False)
    animal_id = db.Column(db.Integer)
    terrarium_id = db.Column(db.Integer)

# Create user model
class User(UserMixin, db.Model):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_active = db.Column(db.Boolean, nullable=False, default=False)
    lang = db.Column(db.String, nullable=False, default="en")

    def __init__(self, email, password, is_admin=False, is_active=False, lang="en"):
        self.email = email
        self.password = generate_password_hash(password)
        self.created_on = datetime.datetime.now()
        self.is_admin = is_admin
        self.is_active = is_active
        self.lang = lang

    def __repr__(self):
        return '<User %r>' % self.email
