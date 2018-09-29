from flask_nav import Nav 
from flask_nav.elements import Navbar, View, Subgroup, Separator

nav = Nav()
nav.register_element('meni', Navbar(
    View('Domača stran', 'index'),
    Subgroup(
        'Naloge',
        View('Vislice', 'index'),
        Separator(),
        View('packarkolize', 'index'),
        ),
    View('Prijava', 'login'),
    View('Registracija', 'register')
))