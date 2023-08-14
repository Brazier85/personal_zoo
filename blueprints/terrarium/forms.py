from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SelectField, DateField
from flask_wtf.file import FileAllowed, FileField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import FileInput

from functions import *

class TerrariumForm(FlaskForm):
    name = StringField(
        "Name", validators=[DataRequired(), Length(min=1, max=40)]
    )
    type = SelectField(
        "Type", validators=[DataRequired()]
    )
    size = StringField(
        "Size", validators=[Length(max=40)]
    )
    notes = TextAreaField(
        "Notes", validators=[]
    )
    image = FileField(
        "Image", validators=[FileAllowed(ALLOWED_EXTENSIONS, 'Images only!')], widget=FileInput()
    )

class EquipmentForm(FlaskForm):
    name = StringField(
        "Name", validators=[DataRequired(), Length(min=1, max=40)]
    )
    text = StringField(
        "Text", validators=[DataRequired()]
    )

class LampsForm(FlaskForm):
    type = StringField(
        "Type", validators=[DataRequired(), Length(min=1, max=40)]
    )
    watt = StringField(
        "Watt"
    )
    position = StringField(
        "Position"
    )
    changed = DateField(
        "Changed"
    )

class EventsForm(FlaskForm):
    event = SelectField(
        "Event", validators=[DataRequired()]
    )
    text = TextAreaField(
        "Text", validators=[DataRequired()]
    )
    date = DateField(
        "Date"
    )