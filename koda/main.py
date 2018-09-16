from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)
app.secret_key = "akshfdgas"

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

if __name__ == "__main__":
    app.run(host="0.0.0.0")
