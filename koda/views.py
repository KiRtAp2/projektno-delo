from main import app, db, fb
from flask import render_template, request, send_from_directory, redirect, url_for, session, abort, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend
from flask_dance.consumer import oauth_authorized, oauth_error
from sqlalchemy.orm.exc import NoResultFound
from random import choice
from os import urandom
from base64 import b64encode
from sqlalchemy import desc

import forms
import models
import vprasanja
from razredi import imena

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

class MyAdminView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated:
            if current_user.admin:
                return True
        else:
            return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

admin = Admin(app, index_view=MyAdminView())
admin.add_view(ModelView(models.User, db.session))

fb.backend = SQLAlchemyBackend(models.OAuth, db.session, user=current_user)

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))

@oauth_authorized.connect_via(fb)
def logged_in(blueprint, token):
    if not token:
            flash("Failed to log in with Facebook.", category="error")
            return False

    resp = blueprint.session.get("me")
    if not resp.ok:
        msg = "Failed to fetch user info from Facebook."
        flash(msg, category="error")
        return False
    info = resp.json()
    user_id = int(info["id"])

    # Find this OAuth token in the database, or create it
    query = models.OAuth.query.filter_by(
        provider=blueprint.name,
        provider_user_id=user_id,
    )
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = models.OAuth(
            provider=blueprint.name,
            provider_user_id=user_id,
            token=token,
        )

    if oauth.user:
        # If this OAuth token already has an associated local account,
        # log in that local user account.
        # Note that if we just created this OAuth token, then it can't
        # have an associated local account yet.
        login_user(oauth.user)
        flash("Successfully signed in with Facebook.")

    else:
        # If this OAuth token doesn't have an associated local account,
        # create a new local user account for this user. We can log
        # in that account as well, while we're at it.
        try:
            email = info["email"]
        except KeyError:
            email = None

        user = models.User(
            email=email,
            username=info["name"],
            password= b64encode(urandom(190)).decode('utf-8'),
            admin=False
        )
        # Associate the new local user account with the OAuth token
        oauth.user = user
        # Save and commit our database models
        db.session.add_all([user, oauth])
        db.session.commit()
        # Log in the new local user account
        login_user(user)
        flash("Successfully signed in with Facebook.")

    return False

@oauth_error.connect_via(fb)
def fb_error(blueprint, error, error_description=None, error_uri=None):
    msg = (
        "OAuth error from {name}! "
        "error={error} description={description} uri={uri}"
    ).format(
        name=blueprint.name,
        error=error,
        description=error_description,
        uri=error_uri,
    )
    flash(msg, category="error")

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
    napake = []
    ne = 0
    post = False

    if request.method == 'GET':
        a = []
        
        if kategorija == 'binarne':
            spojine = vprasanja.dobi_binarne()
        elif kategorija == 'soli':
            spojine = vprasanja.dobi_soli()
        elif kategorija == 'baze':
            spojine = vprasanja.dobi_baze()
        elif kategorija == 'kisline':
            spojine = vprasanja.dobi_kisline()
        elif kategorija == 'kh':
            spojine = vprasanja.dobi_kh()
        else:
            abort(404)
        
        for i in spojine:
            a.append(i.to_dict())
        session['spojine'] = a

    else:
        post = True

        user_odgovori.extend([form.o0.data, form.o1.data, form.o2.data, form.o3.data, form.o4.data])
        spojine = []
        for z in session['spojine']:
            n1 = z['1']['count']
            ime1 = z['1']['simbol']
            n2 = z['2']['count']
            ime2 = z['2']['simbol']
            pravilni.append(imena(ime1, ime2, n1, n2)[0])
            spojine.append(z['formula'])

        if form.validate_on_submit():    
            for j in range(len(user_odgovori)):
                o = user_odgovori[j].split()
                p = pravilni[j].split()
                for n in range(len(o)):
                    try:
                        if o[n].casefold() == p[n].casefold():
                            score += 5
                        else:
                            ne += 1
                    except IndexError:
                        ne += 1
                if ne > 0:
                    napake.append('narobe')
                else:
                    napake.append('')

        if current_user.is_authenticated:
            resp = models.Scores.query.filter_by(user_id=current_user.id).first()
            if resp:
                score += resp.score
                resp.score = score
            else:
                new_score = models.Scores(score=score, user_id=current_user.id)
                db.session.add(new_score)
            db.session.commit()

    return render_template('vprasanja.html', spojine=spojine, score=score, form=form, napake=napake, post=post)

@app.route("/vislice", methods=["GET", "POST"])
def vislice():
    form = forms.Vislice()
    score = 0
    try:
        session['napake']
    except:
        session['napake'] = 0

    if session['napake'] > 10:
        return render_template('vislice.html', spojina='', score=session['score'], form=form, napake='')

    if request.method == 'GET':
        session['score'] = 0
        session['napake'] = 0
    else:
        user_odgovor = form.o0.data
        n1 = session['spojine']['1']['count']
        ime1 = session['spojine']['1']['simbol']
        n2 = session['spojine']['2']['count']
        ime2 = session['spojine']['2']['simbol']
        pravilni = imena(ime1, ime2, n1, n2)[0]

        if form.validate_on_submit():
            o = user_odgovor.split()
            p = pravilni.split()    
            for n in range(len(o)):
                try:
                    if o[n].casefold() == p[n].casefold():
                        score += 5
                    else:
                        session['napake'] += 1
                        break
                except IndexError:
                    session['napake'] += 1
                    break
            session['score'] += score

        if current_user.is_authenticated:
            resp = models.Scores.query.filter_by(user_id=current_user.id).first()
            if resp:
                score += resp.score
                resp.score = score
            else:
                new_score = models.Scores(score=score, user_id=current_user.id)
                db.session.add(new_score)
            db.session.commit()

    moznosti = [vprasanja.dobi_binarne, 
            vprasanja.dobi_soli,
            vprasanja.dobi_baze,
            vprasanja.dobi_kisline,
            vprasanja.dobi_kh
            ]
        
    # spojina = choice(moznosti)(n=1)[0] ----> to bo pol k dodam se ostale elemente v bazo
    spojina = choice(moznosti)(n=1)[0]
    session['spojine'] = spojina.to_dict()

    return render_template('vislice.html', spojina=spojina, score=session['score'], form=form, napake=session['napake'])


@app.route("/lestvica", methods=["GET"])
def lestvica(): #lestvica se ne dela
    najboljsi = db.engine.execute(
        'SELECT User.username, Scores.score FROM Scores JOIN User ON Scores.user_id=User.id ORDER BY Scores.score DESC LIMIT 10')

    print(najboljsi)
    return render_template("scores.html", najboljsi=najboljsi)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = forms.LoginForm()
    if not current_user.is_authenticated:
        if form.validate_on_submit():
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
