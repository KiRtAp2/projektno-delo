from main import app, db, fb
from flask import render_template, request, send_from_directory, redirect, url_for, session, abort, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend
from flask_dance.consumer import oauth_authorized, oauth_error
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from random import choice, getrandbits
from os import urandom
import re
from base64 import b64encode
from sqlalchemy import desc

import forms
import models
import vprasanja
from razredi import konstruiraj

import helpers

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = u"Za dostop do te strani se morate prijaviti!"
login_manager.login_message_category = "error"

# unncomentaj ce hoces dodat admin
# 
# class MyAdminView(AdminIndexView):
#     def is_accessible(self):
#         if current_user.is_authenticated:
#             if current_user.admin:
#                 return True
#             else:
#                 return False
#         else:
#             return False

#     def inaccessible_callback(self, name, **kwargs):
#         return redirect(url_for('login'))

# admin = Admin(app, index_view=MyAdminView(), template_mode='bootstrap3')
# admin.base_template = 'admin/base.html'
# admin.add_view(ModelView(models.User, db.session))
# admin.add_view(ModelView(models.Scores, db.session))
# admin.add_view(ModelView(models.BinarniElement, db.session))
# admin.add_view(ModelView(models.OAuth, db.session))

fb.backend = SQLAlchemyBackend(models.OAuth, db.session, user=current_user)

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))

@app.context_processor
def utility_processor():
    def its_type(obj):
        return type(obj)
    return dict(type=its_type)

@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


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
    mozni = ['Dana so imena spojin. Napišite njihove formule.', 'Dane so formule spojin. Napišite njihova imena.']
    moz = ['ime', 'formula']
    urls = []
    for i in moz:
        urls.append(url_for('izberi_tezavnost', kategorija=kategorija, vrsta='{}'.format(i)))
    return render_template("vrsta.html", moznosti=urls, mozni=mozni)

@app.route("/kviz/<string:kategorija>/<string:vrsta>", methods=['GET'])
def izberi_tezavnost(kategorija, vrsta):
    urls = []
    if kategorija == 'binarne' or kategorija == 'soli':
        for n in range(1, 3):
            urls.append(url_for('kviz', kategorija=kategorija, vrsta=vrsta, tezavnost=n))
    else:
        return redirect(url_for('kviz', kategorija=kategorija, vrsta=vrsta, tezavnost=1))

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
            spojine = vprasanja.dobi_binarne(5, tezavnost)
        elif kategorija == 'soli':
            spojine = vprasanja.dobi_soli(5, tezavnost)
        elif kategorija == 'baze':
            spojine = vprasanja.dobi_baze(5)
        elif kategorija == 'kisline':
            spojine = vprasanja.dobi_kisline(5)
        elif kategorija == 'kh':
            spojine = vprasanja.dobi_kh(5)
        elif kategorija == 'hs':
            spojine = vprasanja.dobi_hidrogensoli(5)
        else:
            abort(404)
        
        for spojina in spojine:
            seznam_spojin.append(spojina.to_dict())
            imena_sp.append(choice(spojina.get_imena()))
        session['spojine'] = seznam_spojin
        session['imena'] = imena_sp
        if vrsta == 'ime':
            return render_template('vprasanja.html', spojine=imena_sp, form=form, vrsta=True, kat=kategorija)
        elif vrsta == 'formula':
            return render_template('vprasanja.html', spojine=spojine, form=form, vrsta=False, kat=kategorija)
        else:
            abort(404)

    else:
        user_odgovori.extend([form.o0.data, form.o1.data, form.o2.data, form.o3.data, form.o4.data])
        spojine = []
        for sp in session['spojine']:
            spojina = konstruiraj(sp)
            spojine.append(spojina.html_prikaz(formatiranje=True))
            pravilna_imena.append(spojina.get_imena())
            if vrsta == 'ime':
                pravilne_formule.append(spojina.html_prikaz(formatiranje=False))

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
                                curr += 1
                            else:
                                ne += 1
                        else:
                            ne += 1
                            user_odgovori[idx] = "/"
                        if curr == 1:
                            break
                    score += curr
                    if (ne > 0 and len(pravilni)==1) or ne > 1:
                        napake.append('narobe')
                    else:
                        napake.append('')

                response = render_template('odgovori.html', spojine=spojine, score=score, form=form, napake=napake, odgovori=user_odgovori, pravilni=pravilna_imena, vrsta=0)

            elif vrsta == 'ime':

                for idx, odgovor in enumerate(user_odgovori):
                    pravilen = pravilne_formule[idx]
                    ne = 0
                    if len(odgovor) != 0:
                        if odgovor == pravilen:
                            score += 1
                        else:
                            ne += 1
                    else:
                        ne += 1
                        user_odgovori[idx] = "/"

                    if ne > 0:
                        napake.append('narobe')
                    else:
                        napake.append('')

                response = render_template('odgovori.html', spojine=pravilna_imena, score=score, form=form, napake=napake, odgovori=user_odgovori, pravilni=spojine, vrsta=1)
        
            helpers.update_score(kategorija=kategorija, current_user=current_user, score=score)

            return response

@app.route("/vislice", methods=["GET", "POST"])
def vislice():
    form = forms.Vislice()
    score = 0
    try:
        session['napake']
    except:
        session['napake'] = 0

    clean = re.compile('<.*?>')

    moznosti = [vprasanja.dobi_binarne,
            vprasanja.dobi_soli,
            vprasanja.dobi_baze,
            vprasanja.dobi_kisline,
            vprasanja.dobi_kh
            ]

    if request.method == 'GET':
        session['score'] = 0
        session['napake'] = 0
        spojina = choice(moznosti)(n=1)[0]
        session['spojine'] = spojina.to_dict()
        session['vrsta'] = getrandbits(1)

        if session['vrsta']:
            pravilna_imena = spojina.get_imena()
            return render_template('vislice.html', spojina=choice(pravilna_imena), score=session['score'], form=form, napake=session['napake'], vrsta=session['vrsta'])
        else:
            html_formula = spojina.html_prikaz(True)
            return render_template('vislice.html', spojina=html_formula, score=session['score'], form=form, napake=session['napake'], vrsta=session['vrsta'])
    
    else:
        user_odgovor = form.o0.data
        spojina = konstruiraj(session['spojine'])

        if form.validate_on_submit():
            if session['vrsta']:
                html_formula = spojina.html_prikaz(True)
                pravilna_formula = spojina.html_prikaz(False)
                if user_odgovor.casefold() == pravilna_formula.casefold():
                    score += 1
                else:
                    session['napake'] += 1

            else:
                pravilna_imena = spojina.get_imena()
                for i, ime in enumerate(pravilna_imena):  
                    if user_odgovor == ime:
                        score += 10
                        break
                    else:
                        if i < len(pravilna_imena)-1:
                            continue
                        else:
                            session['napake'] += 1

            session['score'] += score
            helpers.update_score(kategorija="vse", current_user=current_user, score=score)
    
    if session['napake'] >= 10:
        return render_template('konec.html', score=session['score'], form=form)

    # spojina = choice(moznosti)(n=1)[0] ----> to bo pol k dodamo se ostale elemente v bazo
    spojina = choice(moznosti)(n=1)[0]
    session['spojine'] = spojina.to_dict()
    session['vrsta'] = getrandbits(1)
    if session['vrsta']:
        pravilna_imena = spojina.get_imena()
        return render_template('vislice.html', spojina=choice(pravilna_imena), score=session['score'], form=form, napake=session['napake'], vrsta=session['vrsta'])
    else:
        html_formula = spojina.html_prikaz(True)
        return render_template('vislice.html', spojina=html_formula, score=session['score'], form=form, napake=session['napake'], vrsta=session['vrsta'])


@app.route("/lestvica", methods=["GET", "POST"])
def lestvica(): 

    form = forms.QuerryLeader()

    if request.method == 'GET':
        najboljsi = db.engine.execute(
            'SELECT User.username, Scores.score FROM Scores JOIN User ON Scores.user_id=User.id WHERE Scores.kategorija="total" ORDER BY Scores.score DESC LIMIT 10'
            )
        return render_template("scores.html", najboljsi=najboljsi, form=form)

    elif request.method == 'POST':
        razred = form.izberi_razred.data
        kategorija = form.izberi_kategorijo.data
        if razred == '---' and kategorija == '---':
            topclass = db.engine.execute(
        'SELECT User.username, Scores.score FROM Scores JOIN User ON Scores.user_id=User.id WHERE Scores.kategorija="total" ORDER BY Scores.score DESC LIMIT 10'
        )
        elif kategorija == '---':
            topclass = db.engine.execute(
            'SELECT User.username, Scores.score FROM User JOIN Scores ON User.id=Scores.user_id WHERE User.razred="{}"  AND Scores.kategorija="total" ORDER BY Scores.score DESC LIMIT 10'.format(razred)
            )
        elif razred == '---':
            topclass = db.engine.execute(
            'SELECT User.username, Scores.score FROM User JOIN Scores ON User.id=Scores.user_id WHERE Scores.kategorija="{}" ORDER BY Scores.score DESC LIMIT 10'.format(kategorija)
            )
        else:
            topclass = db.engine.execute(
            'SELECT User.username, Scores.score FROM User JOIN Scores ON User.id=Scores.user_id WHERE User.razred="{}"  AND Scores.kategorija="{}" ORDER BY Scores.score DESC LIMIT 10'.format(razred, kategorija)
            )
        razred = dict(forms.razredi)[razred]
        kategorija = dict(forms.kategorije)[kategorija]

        return render_template("scores.html", najboljsi=topclass, form=form, razred=razred, kategorija=kategorija)


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
                    return render_template('login.html', errors='Napačno geslo!', form=form)
            else:
                return render_template('login.html', errors='Napačno uporabniško ime!', form=form)
    else:
        return redirect(url_for('index'))

    return render_template('login.html', form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = forms.RegisterForm()

    if form.validate_on_submit():
        hashpw = generate_password_hash(form.password.data, method='sha256', salt_length=42)
        new_user = models.User(username=form.username.data, password=hashpw, admin=False, razred=form.razred.data)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            return render_template('register.html', errors='To uporabniško ime je že zasedeno!', form=form)
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
