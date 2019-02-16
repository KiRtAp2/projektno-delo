u"""Datoteka vsebuje osnovne funkcije za postavljanje in preverjanje vprašanj"""


from random import choice as randchoice
import random
from math import gcd

from models import BinarniElement, BazniElement, Kislina, SolniElement, BinarnaIzjema
from razredi import OpisSpojine, OpisBinarne, OpisKisline


def osnovni_seznam(tip_el, tip_iz, opis_sp, n=5):
    seznam = []
    
    def ze_v_seznamu(opis):
        for i in seznam:
            if i == opis:
                return True
        return False

    elementi_1 = tip_el.query.filter(
        tip_el.naboj > 0
    ).all()
    elementi_2 = tip_el.query.filter(
        tip_el.naboj < 0
    ).all()

    izjeme = tip_iz.query.all()

    while len(seznam) < n:
        izbira = randchoice(("element", "izjema"))
        if izbira == "element":
            el1 = randchoice(elementi_1)
            el2 = randchoice(elementi_2)
            lcm = el1.naboj * el2.naboj // gcd(el1.naboj, el2.naboj)
            n_el1 = abs(lcm // el1.naboj)
            n_el2 = abs(lcm // el2.naboj)

            stock_n = abs(el2.naboj * n_el2 // n_el1)

            tip = "obicajna"
            data = {
                "ime1": el1.ime,
                "n1": n_el1,
                "ime2": el2.ime,
                "n2": n_el2,
                "simbol1": el1.simbol,
                "simbol2": el2.simbol,
                "stock_n": stock_n,
            }
        else:
            spojina = randchoice(izjeme)
            tip = "izjema"
            data = {
                "ime": spojina.ime,
                "ime_stock": spojina.ime_stock,
                "formula_raw": spojina.formula,
            }
        opis = opis_sp(tip, data)
        if not ze_v_seznamu(opis):
            seznam.append(opis)

    return seznam


def dobi_binarne(n=5):
    return osnovni_seznam(BinarniElement, BinarnaIzjema, OpisBinarne, n)


def dobi_kisline(n=5):
    seznam = []

    def ze_v_seznamu(opis):
        for i in seznam:
            if i == opis: return True
        return False

    vse_kisline = Kislina.query.all()

    while len(seznam) < n:
        kislina = randchoice(vse_kisline)
        op = OpisKisline({
            "imena": kislina.imena,
            "formula_raw": kislina.formula,
            "tip_spojine": "kislina",
        })
        if not ze_v_seznamu(op):
            seznam.append(op)

    return seznam
