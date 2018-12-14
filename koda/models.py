import main
db = main.db
from flask_login import UserMixin
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), unique=True, nullable=False)
    email = db.Column(db.String(256), unique=True)
    password = db.Column(db.String(256), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)
    razred = db.Column(db.String(2))

    
class Scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship('User',
        backref=db.backref('user', lazy=True))
    

class OAuth(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.Integer, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)


class Element(db.Model):
    """Testno, nima namena biti v končni verziji"""
    id = db.Column(db.Integer, primary_key=True)
    simbol = db.Column(db.String(3), nullable=False)
    ime = db.Column(db.String(20), nullable=False)

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

    
class BinarnaIzjema(db.Model):
    """Binarna spojina, ki se je ne da zapisati z elemeneti"""
    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(50), nullable=False)
    formula = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return "<BinarnaIzjema {}>".format(self.formula)


class BazniElement(db.Model):
    """Element, ki lahko gradi baze"""
    id = db.Column(db.Integer, primary_key=True)
    simbol = db.Column(db.String(3), nullable=False)
    ime = db.Column(db.String(20), nullable=False)
    naboj = db.Column(db.Integer)

    def __repr__(self):
        return "<BazniElement {}>".format(self.simbol)

    
class BaznaIzjema(db.Model):
    """Baza, ki se je ne da zapisati z elementi"""
    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(50), nullable=False)
    formula = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return "<BaznaIzjema {}>".format(self.formula)

    
class Kislina(db.Model):
    """Spojina kislina"""
    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(50), nullable=False)
    formula = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return "<Kislina {}>".format(self.formula)

    
class SolniElement(db.Model):
    """Element, ki lahko gradi sol"""
    id = db.Column(db.Integer, primary_key=True)
    simbol = db.Column(db.String(3), nullable=False)
    ime = db.Column(db.String(20), nullable=False)
    naboj = db.Column(db.Integer)

    def __repr__(self):
        return "<BazniElement {}>".format(self.simbol)

    
class SolnaIzjema(db.Model):
    """Spojina, ki se je ne da zapisati z elementi"""
    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(50), nullable=False)
    formula = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return "<SolnaIzjema {}>".format(self.formula)

