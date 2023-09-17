from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SelectField
from flask_wtf.file import FileAllowed, FileField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import ColorInput, FileInput, TextArea

from functions import *

class AnimalForm(FlaskForm):
    name = StringField(
        lazy_gettext("Name"), validators=[DataRequired(), Length(min=1, max=40)]
    )
    art = SelectField(
        lazy_gettext("Type"), validators=[DataRequired()]
    )
    morph = StringField(
        lazy_gettext("Morph"), validators=[Length(max=40)]
    )
    gender = SelectField(
        lazy_gettext("Gender"), validators=[DataRequired()]
    )
    birth = StringField(
        lazy_gettext("Birth"), validators=[Length(max=40)]
    )
    notes = TextAreaField(
        lazy_gettext("Notes"), widget=TextArea()
    )
    image = FileField(
        lazy_gettext("Image"), validators=[FileAllowed(ALLOWED_EXTENSIONS, 'Images only!')], widget=FileInput()
    )
    background_color = StringField(
        lazy_gettext("Background Color"),  widget=ColorInput()
    )
    default_ft = SelectField(
        lazy_gettext("Default feeding type")
    )
    terrarium = SelectField(
        lazy_gettext("Terrarium")
    )