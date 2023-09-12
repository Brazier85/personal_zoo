from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired

from functions import *

class HistoryForm(FlaskForm):
    date = DateField(
        lazy_gettext("Date"), validators=[DataRequired()]
    )
    event = SelectField(
        lazy_gettext("Event/Action")
    )
    text = TextAreaField(
        lazy_gettext("Text")
    )


class HistoryMultiForm(FlaskForm):
    date = DateField(
        lazy_gettext("Date"), validators=[DataRequired()]
    )
    event = SelectField(
        lazy_gettext("Event/Action")
    )
    text = TextAreaField(
        lazy_gettext("Text")
    )
    animals = SelectMultipleField(
        lazy_gettext("Animals"), coerce=int
    )
    terrariums = SelectMultipleField(
        lazy_gettext("Terrariums"), coerce=int
    )