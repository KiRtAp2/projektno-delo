from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from navbar import nav
from flask_login import UserMixin
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin

app = Flask(__name__)
app.config.from_envvar('YOURAPPLICATION_SETTINGS')

Bootstrap(app)

db = SQLAlchemy()
db.init_app(app)

nav.init_app(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), unique=True, nullable=False)
    email = db.Column(db.String(256), unique=True)
    password = db.Column(db.String(256))
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

class OAuth(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.Integer, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)


from views import *

from oauth.github import github_bp
app.register_blueprint(github_bp, url_prefix="/login/github")

if __name__ == "__main__":

    app.run(host="0.0.0.0")
