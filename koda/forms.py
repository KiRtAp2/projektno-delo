from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(),Length(min=4, max=20)])
    password = PasswordField('password', validators=[InputRequired(),Length(min=8, max=80)])
    email = StringField('email', validators=[Email(),Length(max=80),InputRequired()])

class Vprasanja(FlaskForm):
	o0 = StringField('ime spojine')
	o1 = StringField('ime spojine')
	o2 = StringField('ime spojine')
	o3 = StringField('ime spojine')
	o4 = StringField('ime spojine')

class Vislice(FlaskForm):
    o0 = StringField('ime spojine')