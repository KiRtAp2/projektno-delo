from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from navbar import nav
from sys import argv


app = Flask(__name__)
app.config.from_envvar('YOURAPPLICATION_SETTINGS')

Bootstrap(app)

db = SQLAlchemy()
db.init_app(app)

nav.init_app(app)

from views import *

if __name__ == "__main__":

    if "--db-create-all" in argv or "-db" in argv:
        with app.app_context():
            db.create_all()
        quit()
    
    app.run(host="0.0.0.0")
