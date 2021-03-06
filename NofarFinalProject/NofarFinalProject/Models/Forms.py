from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms import Form, BooleanField, PasswordField
from wtforms import TextField, TextAreaField, SelectField
from wtforms import validators, ValidationError
from wtforms.fields.html5 import DateField

from wtforms.validators import DataRequired
from wtforms.validators import InputRequired


class ExpandForm(FlaskForm):
	submit1 = SubmitField('Expand')
	name="Expand"
	value="Expand"

class CollapseForm(FlaskForm):
	submit2 = SubmitField('Collapse')
	name="Collapse"
	value="Collapse"

class YomLayla(FlaskForm):
    yl = RadioField('Choose Day or Night:' , validators = [DataRequired] , choices=[('1', 'Day'), ('5', 'Night')])
    subnmit = SubmitField('Submit')