from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField
from wtforms.validators import DataRequired, Email, ValidationError
from wtforms.fields.html5 import EmailField
import re


def my_length_check(form, field):
    if not re.search("^((\+7|7|8)+([0-9]){10})$", field.data):
        raise ValidationError('Field must be phone number')


class ClientForm(FlaskForm):
    fio = StringField('fio', validators=[DataRequired()])
    phone = StringField('phone', validators=[DataRequired(), my_length_check])
    email = EmailField('email', validators=[DataRequired(), Email()])
    photo = FileField('photo', validators=[])
