from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import InputRequired, Email, Length, EqualTo

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
    username = StringField('uporabniško ime', validators=[InputRequired(message='To polje ne sme biti prazno!'), Length(min=4, max=20, message='Uporabniško ime mora biti dolgo med 4 in 20 znaki!')])
    password = PasswordField('geslo', validators=[InputRequired(message='To polje ne sme biti prazno!'), Length(min=8, max=80, message='Geslo mora biti dolgo vsaj 8 znakov!')])
    remember = BooleanField('zapomni si me')

class RegisterForm(FlaskForm):
    username = StringField('uporabniško ime', validators=[InputRequired(message='To polje ne sme biti prazno!'),Length(min=4, max=20, message='Uporabniško ime mora biti dolgo med 4 in 20 znaki!')])
    password = PasswordField('geslo', validators=[InputRequired(message='To polje ne sme biti prazno!'),Length(min=8, max=80, message='Geslo mora biti dolgo vsaj 8 znakov!'), EqualTo('potrdi geslo', message='Gesli se ne ujemata!')])
    razred = SelectField('razred', choices=razredi)

class Vprasanja(FlaskForm):
	o0 = StringField('')
	o1 = StringField('')
	o2 = StringField('')
	o3 = StringField('')
	o4 = StringField('')

class Vislice(FlaskForm):
    o0 = StringField('')

class QuerryRazred(FlaskForm):
    razred = SelectField('Razred', choices=razredi)

class QuerryLeader(FlaskForm):
    izberi_razred = SelectField('Razred', choices=razredi)
    izberi_kategorijo = SelectField('Kategorija', choices=kategorije)


