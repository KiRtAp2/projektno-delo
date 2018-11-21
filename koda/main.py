from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
from navbar import nav
from sys import argv
import json


app = Flask(__name__)
app.config.from_envvar('YOURAPPLICATION_SETTINGS')

Bootstrap(app)

db = SQLAlchemy()
db.init_app(app)

nav.init_app(app)
try:
    with open('keys.json') as f:
        data = json.load(f)
        fb = make_facebook_blueprint(
            client_id=data['fb']['id'],
            client_secret=data['fb']['key'],
            scope="email",
        )
except FileNotFoundError:
    print("Datoteka keys.json ni bilo mogoče najti. Si prepričan, da jo imaš?")
    raise
app.register_blueprint(fb, url_prefix="/login/facebook")

from views import *

if __name__ == "__main__":

    if "--db-create-all" in argv or "-db" in argv:
        with app.app_context():
            db.create_all()
        quit()
    
    app.run(host="0.0.0.0")
