from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import InputRequired, Email, Length

crke = ['A', 'B', 'C', 'D', 'E', 'F']
razredi = [('---', '---')]
for i in range(1, 5):
    for c in crke:
        razredi.append(('{}{}'.format(i,c), '{}.{}'.format(i,c)))
kategorije=[('---', '---'),
    ('binarne','Binarne spojine'),
    ('soli','Soli'),
    ('baze','Baze'),
    ('kisline','Kisline'),
    ('kh','Kristalohidrati'),
    ('hs','Hidrogensoli'),
    ('vislice','Vislice')
]

class LoginForm(FlaskForm):
    username = StringField('uporabniško ime', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('geslo', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('zapomni si me')

class RegisterForm(FlaskForm):
    username = StringField('uporabniško ime', validators=[InputRequired(),Length(min=4, max=20)])
    password = PasswordField('geslo', validators=[InputRequired(),Length(min=8, max=80)])
    razred = SelectField('razred', choices=razredi)

class Vprasanja(FlaskForm):
	o0 = StringField('')
	o1 = StringField('')
	o2 = StringField('')
	o3 = StringField('')
	o4 = StringField('')

class Vislice(FlaskForm):
    o0 = StringField('ime spojine')

class QuerryLeader(FlaskForm):
    izberi_razred = SelectField('Razred', choices=razredi)
    izberi_kategorijo = SelectField('Kategorija', choices=kategorije)


