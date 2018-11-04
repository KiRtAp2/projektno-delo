import main
db = main.db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), unique=True, nullable=False)
    email = db.Column(db.String(256), unique=True)
    password = db.Column(db.String(256), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)

    
class Scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship('User',
        backref=db.backref('user', lazy=True))


    
class Element(db.Model):
    """Testno, nima namena biti v končni verziji"""
    id = db.Column(db.Integer, primary_key=True)
    simbol = db.Column(db.String(3), unique=True, nullable=False)
    ime = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return "<Element {}>".format(self.simbol)

    
class BinarniElement(db.Model):
    """Element, ki lahko gradi binarne spojine"""
    id = db.Column(db.Integer, primary_key=True)
    simbol = db.Column(db.String(3), unique=True, nullable=False)
    ime = db.Column(db.String(20), unique=True, nullable=False)
    naboj = db.Column(db.Integer)

    def __repr__(self):
        return "<BinarniElement {}>".format(self.simbol)


class BazniElement(db.Model):
    """Element, ki lahko gradi baze"""
    id = db.Column(db.Integer, primary_key=True)
    simbol = db.Column(db.String(3), unique=True, nullable=False)
    ime = db.Column(db.String(20), unique=True, nullable=False)
    naboj = db.Column(db.Integer)

    def __repr__(self):
        return "<BazniElement {}>".format(self.simbol)

    
class KisliElement(db.Model):
    """Element, ki lahko gradi kisline"""
    id = db.Column(db.Integer, primary_key=True)
    simbol = db.Column(db.String(3), unique=True, nullable=False)
    ime = db.Column(db.String(20), unique=True, nullable=False)
    naboj = db.Column(db.Integer)

    def __repr__(self):
        return "<KisliElement {}>".format(self.simbol)

    
class SolniElement(db.Model):
    """Element, ki lahko gradi sol"""
    id = db.Column(db.Integer, primary_key=True)
    simbol = db.Column(db.String(3), unique=True, nullable=False)
    ime = db.Column(db.String(20), unique=True, nullable=False)
    naboj = db.Column(db.Integer)

    def __repr__(self):
        return "<BazniElement {}>".format(self.simbol)
