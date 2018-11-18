from flask_nav import Nav 
from flask_nav.elements import Navbar, View, Subgroup, Separator, Text, Link, RawTag
from flask_login import current_user

class UserGreeting(Text):
    def __init__(self):
        pass

    @property
    def text(self):
        if current_user:
            username = current_user.username
        else:
            username = ''
        return username

nav = Nav()
login_bar = Navbar(
    View('Domača stran', 'index'),
    Subgroup(
        'Naloge',
        View('Vislice', 'vislice'),
        Separator(),
        View('Binarne spojine', 'kviz', kategorija='binarne'),
        View('Soli', 'kviz', kategorija='soli'),
        View('Baze', 'kviz', kategorija='baze'),
        View('Kisline', 'kviz', kategorija='kisline'),
        View('Kristalohidrati', 'kviz', kategorija='kh'),
        ),
    View('Lestvica', 'lestvica'),
    View('Prijava', 'login'),
    View('Registracija', 'register')
)

logout_bar = Navbar(
    View('Domača stran', 'index'),
    Subgroup(
        'Naloge',
        View('Vislice', 'vislice'),
        Separator(),
        View('Binarne spojine', 'kviz', kategorija='binarne'),
        View('Soli', 'kviz', kategorija='soli'),
        View('Baze', 'kviz', kategorija='baze'),
        View('Kisline', 'kviz', kategorija='kisline'),
        View('Kristalohidrati', 'kviz', kategorija='kh'),
        ),
    View('Lestvica', 'lestvica'),
    View('Odjava', 'logout'),
    UserGreeting()
)

nav.register_element('login_bar', login_bar)
nav.register_element('logout_bar', logout_bar)