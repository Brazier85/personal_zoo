from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SelectField, DateField
from flask_wtf.file import FileAllowed, FileField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import FileInput

from functions import *

class TerrariumForm(FlaskForm):
    name = StringField(
        lazy_gettext("Name"), validators=[DataRequired(), Length(min=1, max=40)]
    )
    type = SelectField(
        lazy_gettext("Type"), validators=[DataRequired()]
    )
    size = StringField(
        lazy_gettext("Size"), validators=[Length(max=40)]
    )
    notes = TextAreaField(
        lazy_gettext("Notes"), validators=[]
    )
    image = FileField(
        lazy_gettext("Image"), validators=[FileAllowed(ALLOWED_EXTENSIONS, 'Images only!')], widget=FileInput()
    )

class EquipmentForm(FlaskForm):
    name = StringField(
        lazy_gettext("Name"), validators=[DataRequired(), Length(min=1, max=40)]
    )
    text = StringField(
        lazy_gettext("Text"), validators=[DataRequired()]
    )

class LampsForm(FlaskForm):
    type = StringField(
        lazy_gettext("Type"), validators=[DataRequired(), Length(min=1, max=40)]
    )
    watt = StringField(
        lazy_gettext("Watt")
    )
    position = StringField(
        lazy_gettext("Position")
    )
    changed = DateField(
        lazy_gettext("Changed")
    )

class EventsForm(FlaskForm):
    event = SelectField(
        lazy_gettext("Event"), validators=[DataRequired()]
    )
    text = TextAreaField(
        lazy_gettext("Text"), validators=[DataRequired()]
    )
    date = DateField(
        lazy_gettext("Date")
    )