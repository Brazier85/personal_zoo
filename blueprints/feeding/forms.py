from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, StringField, SelectField, DateField, IntegerField
from wtforms.validators import DataRequired
from wtforms.widgets import html_params

from functions import *

class FeedingForm(FlaskForm):
    date = DateField(
        "Date", validators=[DataRequired()]
    )
    type = SelectField(
        "Type"
    )
    count = IntegerField(
        "Count"
    )
    unit = StringField(
        "Unit"
    )


class FeedingMultiForm(FlaskForm):
    date = DateField(
        "Date", validators=[DataRequired()]
    )
    type = SelectField(
        "Type"
    )
    count = IntegerField(
        "Count"
    )
    unit = StringField(
        "Unit"
    )
    animals = SelectMultipleField(
        "Animals", coerce=int
    )
    terrariums = SelectMultipleField(
        "Terrariums", coerce=int
    )