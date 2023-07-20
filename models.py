from flask_sqlalchemy import SQLAlchemy
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
    art = db.db.Column(db.Integer, db.ForeignKey('AnimalType.id'))
    morph = db.Column(db.String)
    gender = db.Column(db.String)
    birth = db.Column(db.Date)
    notes = db.Column(db.String)
    image = db.Column(db.String)
    background_color = db.Column(db.String)
    created_date = db.Column(db.Date, default=datetime.datetime.utcnow)
    updated_date = db.Column(db.Date, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Animal %r>' % self.name

class Feeding(db.Model):
    __tablename__ = 'feeding'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    animal = db.Column(db.Integer)
    type = db.Column(db.String)
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
