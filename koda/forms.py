from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import InputRequired, Email, Length

crke = ['A', 'B', 'C', 'D', 'E', 'F']
razredi = []
for i in range(1, 5):
    for c in crke:
        razredi.append(('{}{}'.format(i,c), '{}.{}'.format(i,c)))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(),Length(min=4, max=20)])
    password = PasswordField('password', validators=[InputRequired(),Length(min=8, max=80)])
    email = StringField('email', validators=[Email(),Length(max=80),InputRequired()])
    razred = SelectField('Razred', choices=razredi)

class Vprasanja(FlaskForm):
	o0 = StringField('ime spojine')
	o1 = StringField('ime spojine')
	o2 = StringField('ime spojine')
	o3 = StringField('ime spojine')
	o4 = StringField('ime spojine')

class Vislice(FlaskForm):
    o0 = StringField('ime spojine')

class QuerryRazred(FlaskForm):
    razred = SelectField('Razred', choices=razredi)