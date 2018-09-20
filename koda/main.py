from flask import Flask
<<<<<<< HEAD
=======
from flask import render_template, request, send_from_directory

import baza
>>>>>>> 42355c47a498e7ba1c0d640d6b193b4d41d14e0c

app = Flask(__name__)
from views import *

<<<<<<< HEAD
=======
@app.route("/debug", methods=["GET"])
def debug():
    e = baza.get_elementi()
    f = []
    for l in e:
        f.append(l[0])
    return render_template("domaca_stran.html", spojine=f, prou=None)

# TEGA SE NE DELA V PRODUCTIONU - TO JE SAMO ZA DEBUG
@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory('static', path)
    
>>>>>>> 42355c47a498e7ba1c0d640d6b193b4d41d14e0c

if __name__ == "__main__":
    app.run(host="0.0.0.0")
