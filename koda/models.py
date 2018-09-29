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

    
class Element(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    simbol = db.Column(db.String(3), unique=True, nullable=False)
    ime = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return "<Element {}>".format(self.simbol)
