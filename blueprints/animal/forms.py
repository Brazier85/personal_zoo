from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SelectField
from flask_wtf.file import FileAllowed, FileField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import ColorInput, FileInput

from functions import *

class AnimalForm(FlaskForm):
    name = StringField(
        "Name", validators=[DataRequired(), Length(min=1, max=40)]
    )
    art = SelectField(
        "Type", validators=[DataRequired()]
    )
    morph = StringField(
        "Morph", validators=[Length(max=40)]
    )
    gender = SelectField(
        "Gender", validators=[DataRequired()]
    )
    birth = StringField(
        "Birth", validators=[Length(max=40)]
    )
    notes = TextAreaField(
        "Notes"
    )
    image = FileField(
        "Image", validators=[FileAllowed(ALLOWED_EXTENSIONS, 'Images only!')], widget=FileInput()
    )
    background_color = StringField(
        "Background Color",  widget=ColorInput()
    )
    default_ft = SelectField(
        "Default feeding type"
    )
    terrarium = SelectField(
        "Terrarium"
    )