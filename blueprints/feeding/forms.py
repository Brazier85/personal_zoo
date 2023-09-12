from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, StringField, SelectField, DateField, IntegerField
from wtforms.validators import DataRequired
from wtforms.widgets import html_params

from functions import *

class FeedingForm(FlaskForm):
    date = DateField(
        lazy_gettext("Date"), validators=[DataRequired()]
    )
    type = SelectField(
        lazy_gettext("Type")
    )
    count = IntegerField(
        lazy_gettext("Count")
    )
    unit = StringField(
        lazy_gettext("Unit")
    )


class FeedingMultiForm(FlaskForm):
    date = DateField(
        lazy_gettext("Date"), validators=[DataRequired()]
    )
    type = SelectField(
        lazy_gettext("Type")
    )
    count = IntegerField(
        lazy_gettext("Count")
    )
    unit = StringField(
        lazy_gettext("Unit")
    )
    animals = SelectMultipleField(
        lazy_gettext("Animals"), coerce=int
    )
    terrariums = SelectMultipleField(
        lazy_gettext("Terrariums"), coerce=int
    )