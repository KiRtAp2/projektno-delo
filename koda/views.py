from main import app, db, fb
from flask import render_template, request, send_from_directory, redirect, url_for, session, abort, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend
from flask_dance.consumer import oauth_authorized, oauth_error
from sqlalchemy.orm.exc import NoResultFound
from random import choice, getrandbits
from os import urandom
import re
from base64 import b64encode
from sqlalchemy import desc

import forms
import models
import vprasanja
from razredi import konstruiraj

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
        else:
            return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

admin = Admin(app, index_view=MyAdminView(), template_mode='bootstrap3')
# admin.base_template = 'admin/base.html'
admin.add_view(ModelView(models.User, db.session))
admin.add_view(ModelView(models.Scores, db.session))
admin.add_view(ModelView(models.BinarniElement, db.session))
admin.add_view(ModelView(models.OAuth, db.session))

fb.backend = SQLAlchemyBackend(models.OAuth, db.session, user=current_user)

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))

@app.context_processor
def utility_processor():
    def its_type(obj):
        return type(obj)
    return dict(type=its_type)

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
            admin=False,
            razred=None
        )
        # Associate the new local user account with the OAuth token
        oauth.user = user
        # Save and commit our database models
        db.session.add_all([user, oauth])
        db.session.commit()
        # Log in the new local user account
        login_user(user)

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
    return render_template("domaca_stran.html")

@app.route("/kviz", methods=['GET'])
def izberi_kategorijo():
    return render_template("kviz.html")

@app.route("/kviz/<string:kategorija>", methods=['GET'])
def izberi_vrsto(kategorija):
    mozni = ['ime', 'formula']
    urls = []
    for i in mozni:
        urls.append(url_for('izberi_tezavnost', kategorija=kategorija, vrsta='{}'.format(i)))
    return render_template("vrsta.html", moznosti=urls, mozni=mozni)

@app.route("/kviz/<string:kategorija>/<string:vrsta>", methods=['GET'])
def izberi_tezavnost(kategorija, vrsta):
    urls = []
    for n in range(1, 4):
        urls.append(url_for('kviz', kategorija=kategorija, vrsta=vrsta, tezavnost=n))
    return render_template("tezavnost.html", moznosti=urls)

@app.route("/kviz/<string:kategorija>/<string:vrsta>/<int:tezavnost>", methods=["GET", "POST"])
def kviz(kategorija, vrsta, tezavnost):
    form = forms.Vprasanja()
    user_odgovori = []
    pravilna_imena = []
    pravilne_formule = []
    score = 0
    napake = []
    ne = 0
    post = False

    clean = re.compile('<.*?>')

    if request.method == 'GET':
        seznam_spojin = []
        imena_sp = []
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
        
        for spojina in spojine:
            seznam_spojin.append(spojina.to_dict())
            imena_sp.append(choice(spojina.get_imena()))
        session['spojine'] = seznam_spojin
        session['imena'] = imena_sp
        if vrsta == 'ime':
            return render_template('vprasanja.html', spojine=imena_sp, form=form)
        elif vrsta == 'formula':
            return render_template('vprasanja.html', spojine=spojine, form=form)
        else:
            abort(404)

    else:
        post = True

        user_odgovori.extend([form.o0.data, form.o1.data, form.o2.data, form.o3.data, form.o4.data])
        spojine = []
        for sp in session['spojine']:
            spojina = konstruiraj(sp)
            spojine.append(spojina.html_prikaz())
            pravilna_imena.append(spojina.get_imena())
            if vrsta == 'ime':
                pravilne_formule.append(re.sub(clean, '', spojina.html_prikaz()))

        if vrsta == 'ime':
            pravilna_imena = session['imena']


        if form.validate_on_submit():
            if vrsta == 'formula':
                for idx, odgovor in enumerate(user_odgovori):
                    pravilni = pravilna_imena[idx]
                    ne = 0
                    curr = 0
                    for pravilen in pravilni:
                        if len(odgovor) != 0:
                            if odgovor.casefold() == pravilen.casefold():
                                curr += 10
                            else:
                                ne += 1
                        else:
                            ne += 1
                            user_odgovori[idx] = "/"
                        if curr == 10:
                            break
                    score += curr
                    if ne-1 > 0:
                        napake.append('narobe')
                    else:
                        napake.append('')

                response = render_template('odgovori.html', spojine=spojine, score=score, form=form, napake=napake, odgovori=user_odgovori, pravilni=pravilna_imena)

            elif vrsta == 'ime':

                for idx, odgovor in enumerate(user_odgovori):
                    pravilen = pravilne_formule[idx]
                    ne = 0
                    if len(odgovor) != 0:
                        if odgovor.casefold() == pravilen.casefold():
                            score += 10
                        else:
                            ne += 1
                    else:
                        ne += 1
                        user_odgovori[idx] = "/"

                    if ne > 0:
                        napake.append('narobe')
                    else:
                        napake.append('')

                response = render_template('odgovori.html', spojine=pravilna_imena, score=score, form=form, napake=napake, odgovori=user_odgovori, pravilni=spojine)
        
            if current_user.is_authenticated and score:
                resp = models.Scores.query.filter_by(user_id=current_user.id, kategorija=kategorija).first()
                total = models.Scores.query.filter_by(user_id=current_user.id, kategorija="total").first()
                if resp:
                    resp.score += score
                else:
                    new_score = models.Scores(score=score, user_id=current_user.id, kategorija=kategorija)
                    db.session.add(new_score)

                if total:
                    total.score += score
                else:
                    new_total = models.Scores(score=score, user_id=current_user.id, kategorija="total")
                    db.session.add(new_total)
                db.session.commit()

            return response

@app.route("/vislice", methods=["GET", "POST"])
def vislice():
    form = forms.Vislice()
    score = 0
    prej_prov = False
    try:
        session['napake']
    except:
        session['napake'] = 0

    if request.method == 'GET':
        session['score'] = 0
        session['napake'] = 0
    else:
        user_odgovor = form.o0.data
        spojina = konstruiraj(sp)
        html_formula = spojina.html_prikaz()
        pravilna_imena = spojina.get_imena()
        pravilna_formula = re.sub(clean, '', spojina.html_prikaz())

        index = getrandbits(1)

        pravilno = (pravilna_imena, pravilna_formula)[index]

        if form.validate_on_submit():
            if index:
                if user_odgovor.casefold() == pravilna_formula.casefold():
                    score += 10
                else:
                    session['napake'] += 1

                response = render_template('vislice.html', spojina=choice(pravilna_imena), score=session['score'], form=form, napake=session['napake'])

            else:
                for i, ime in enumerate(pravilna_imena):  
                    if user_odgovor.casefold() == ime.casefold():
                        score += 10
                        break
                    else:
                        if i < len(pravilna_imena)-1:
                            continue
                        else:
                            session['napake'] += 1
                response = render_template('vislice.html', spojina=html_formula, score=session['score'], form=form, napake=session['napake'])

            session['score'] += score

    moznosti = [vprasanja.dobi_binarne
            # vprasanja.dobi_soli,
            # vprasanja.dobi_baze,
            # vprasanja.dobi_kisline,
            # vprasanja.dobi_kh
            ]
        
    # spojina = choice(moznosti)(n=1)[0] ----> to bo pol k dodamo se ostale elemente v bazo
    spojina = choice(moznosti)(n=1)[0]
    session['spojine'] = spojina.to_dict()

    if session['napake'] >= 10:
        if current_user.is_authenticated and session['score']:
            resp = models.Scores.query.filter_by(user_id=current_user.id, kategorija="vse").first()
            total = models.Scores.query.filter_by(user_id=current_user.id, kategorija="total").first()
            if resp:
                resp.score += session['score']
            else:
                new_score = models.Scores(score=score, user_id=current_user.id, kategorija="vse")
                db.session.add(new_score)

            if total:
                total.score += session['score']
            else:
                new_total = models.Scores(score=score, user_id=current_user.id, kategorija="total")
                db.session.add(new_total)
            db.session.commit()

        return render_template('konec.html', score=session['score'], form=form)

    return response


@app.route("/lestvica", methods=["GET", "POST"])
def lestvica(): #lestvica se ne dela
    najboljsi = db.engine.execute(
        'SELECT User.username, Scores.score FROM Scores JOIN User ON Scores.user_id=User.id WHERE Scores.kategorija="total" ORDER BY Scores.score DESC LIMIT 10'
        )
    form = forms.QuerryRazred()

    if request.method == 'POST':
        razred = form.razred.data
        if razred == '---':
            topclass = najboljsi
        else:
            topclass = db.engine.execute(
            'SELECT User.username, Scores.score FROM User JOIN Scores ON User.id=Scores.user_id WHERE User.razred="{}"  AND Scores.kategorija="total" ORDER BY Scores.score DESC LIMIT 10'.format(razred)
            )
        return render_template("scores.html", najboljsi=topclass, form=form, razred=razred)

    return render_template("scores.html", najboljsi=najboljsi, form=form)

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
        new_user = models.User(username=form.username.data, password=hashpw, email=form.email.data, admin=False, razred=form.razred.data)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('index'))

    return render_template('register.html', form=form)

@app.route("/logout", methods=["GET"])

@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@login_required
@app.route('/razred', methods=["GET", "POST"])
def dodaj_razred():
    form = forms.QuerryRazred()
    if current_user.razred == None:
        if request.method == 'POST':
            current_user.razred = form.razred.data
            db.session.add(current_user)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return render_template('razred.html', form=form)
    else:
        return redirect(url_for('index'))

# TEGA SE NE DELA V PRODUCTIONU - TO JE SAMO ZA DEBUG
@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory('static', path)
