from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FileField
from wtforms.validators import DataRequired
from wtforms.widgets import html_params

from functions import *

class DocumentForm(FlaskForm):
    name = StringField(
        "Name", validators=[DataRequired()]
    )
    filename = FileField(
        "File"
    )