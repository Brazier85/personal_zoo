from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired

from functions import *

class HistoryForm(FlaskForm):
    date = DateField(
        "Date", validators=[DataRequired()]
    )
    event = SelectField(
        "Event/Action"
    )
    text = TextAreaField(
        "Text"
    )


class HistoryMultiForm(FlaskForm):
    date = DateField(
        "Date", validators=[DataRequired()]
    )
    event = SelectField(
        "Event/Action"
    )
    text = TextAreaField(
        "Text"
    )
    animals = SelectMultipleField(
        "Animals", coerce=int
    )
    terrariums = SelectMultipleField(
        "Terrariums", coerce=int
    )