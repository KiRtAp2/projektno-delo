from main import app, db
from flask import render_template, request, send_from_directory, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView


import forms
import models
import vprasanja
from razredi import ime

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

class MyAdminView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated:
            if current_user.username in admins:
                return True
        else:
            return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

admin = Admin(app, index_view=MyAdminView())
admin.add_view(ModelView(models.User, db.session))

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))

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


@app.route("/kviz/<string:kategorija>", methods=["GET", "POST"])
def kviz(kategorija):
    form = forms.Vprasanja()
    user_odgovori = []
    pravilni = []
    score = 0
    allowed = {
        'vprasanja.dobi_binarne': vprasanja.dobi_binarne,
        'vprasanja.dobi_soli': vprasanja.dobi_soli,
        'vprasanja.dobi_kisline': vprasanja.dobi_kisline,
        'vprasanja.dobi_baze': vprasanja.dobi_baze,
        'vprasanja.dobi_kh': vprasanja.dobi_kh
       }
    if request.method == 'GET':
        a = []
        funkcija = eval('vprasanja.dobi_{}'.format(kategorija), {}, allowed)
        spojine = funkcija()
        print(spojine)
        for i in spojine:
            a.append(i.to_dict())
        session['spojine'] = a
    else:
        user_odgovori.extend([form.o0.data, form.o1.data, form.o2.data, form.o3.data, form.o4.data])
        spojine = []
        for z in session['spojine']:
            n1 = z['1']['count']
            ime1 = z['1']['simbol']
            n2 = z['2']['count']
            ime2 = z['2']['simbol']
            pravilni.append(ime(ime1, ime2, n1, n2))
            print(ime(ime1, ime2, n1, n2))
            spojine.append(z['formula'])

        if form.validate_on_submit():    
            for j in range(len(user_odgovori)):
                o = user_odgovori[j].split()
                p = pravilni[j].split()
                for n in range(len(o)):
                    if o[n] == p[n]:
                        score += 5

    return render_template('vprasanja.html', spojine=spojine, score=score, form=form)

@app.route("/vislice", methods=["GET"])
def vislice():
    pass

@app.route("/lestvica", methods=["GET"])
def lestvica():
    pass

@app.route("/login", methods=["GET", "POST"])
def login():
    form = forms.LoginForm()
    if not current_user.is_authenticated:
        if form.validate_on_submit():
            print(form.username.data)
            user = models.User.query.filter_by(username=form.username.data).first()
            if user:
                if check_password_hash(user.password, form.password.data):
                    login_user(user, remember=form.remember.data)
                    return redirect(url_for('index'))
                else:
                    return 'invalid password'
            else:
                return 'invalid username'
    else:
        return redirect(url_for('index'))

    return render_template('login.html', form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        hashpw = generate_password_hash(form.password.data, method='sha256', salt_length=42)
        new_user = models.User(username=form.username.data, password=hashpw, email=form.email.data, admin=False)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('register.html', form=form)

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# TEGA SE NE DELA V PRODUCTIONU - TO JE SAMO ZA DEBUG
@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory('static', path)
