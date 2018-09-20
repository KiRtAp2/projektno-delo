from main import app
from flask import render_template, request, send_from_directory
import baza

@app.route("/", methods=['GET', 'POST'])
def index():
    
    prou = None
    pravilni=[]
    if request.method == 'POST':
        odgovori = [request.form['ime1'],
        request.form['ime2'],
        request.form['ime3']]
        if odgovori == pravilni:
            prou=True
        else:
            prou = False

    spojine=["a","bb","c"]
    # spojine je list spojin
    return render_template("domaca_stran.html", spojine=spojine, prou=prou)

@app.route("/debug", methods=["GET"])
def debug():
    e = baza.get_elementi()
    f = []
    for l in e:
        f.append(l[0])
    return render_template("domaca_stran.html", spojine=f, prou=None)

@app.route("/kviz", methods=["GET"])
def kviz():
    pass

@app.route("/vislice", methods=["GET"])
def vislice():
    pass

@app.route("/lestvica", methods=["GET"])
def lestvica():
    pass

# TEGA SE NE DELA V PRODUCTIONU - TO JE SAMO ZA DEBUG
@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory('static', path)