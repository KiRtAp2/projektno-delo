u"""Datoteka vsebuje osnovne funkcije za postavljanje in preverjanje vprašanj"""


from random import choice as randchoice
from math import gcd

from models import BinarniElement, Kislina, SolniElement, SolnaIzjema, BinarnaIzjema, Baza, HidrogensolniElement, Kristalohidrat
from razredi import OpisSpojine, OpisBinarne, OpisKisline, OpisBaze, OpisSoli, OpisHidrogensoli, OpisKristalohidrata


def osnovni_seznam(tip_el, tip_iz, opis_sp, n, tez):
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
        if tez==1 or len(izjeme) == 0:
            el1 = randchoice(elementi_1)
            el2 = randchoice(elementi_2)
            lcm = el1.naboj * el2.naboj // gcd(el1.naboj, el2.naboj)
            n_el1 = abs(lcm // el1.naboj)
            n_el2 = abs(lcm // el2.naboj)

            stock_n = abs(el2.naboj * n_el2 // n_el1)

            tip = "obicajna"
            data = {
                "ime1": el1.imena,
                "n1": n_el1,
                "ime2": el2.imena,
                "n2": n_el2,
                "simbol1": el1.simbol,
                "simbol2": el2.simbol,
                "stock_n": stock_n,
            }
        else:
            spojina = randchoice(izjeme)
            tip = "izjema"
            data = {
                "imena": spojina.imena,
                "formula_raw": spojina.formula,
            }
        opis = opis_sp(tip, data)
        if not ze_v_seznamu(opis):
            seznam.append(opis)

    return seznam


def dobi_binarne(n=5, tez=1):
    return osnovni_seznam(BinarniElement, BinarnaIzjema, OpisBinarne, n, tez)


def dobi_kisline(n=5, tez=1):
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


def dobi_baze(n=5, tez=1):
    seznam = []

    def ze_v_seznamu(opis):
        for i in seznam:
            if i == opis: return True
        return False

    vse_baze = Baza.query.all()

    while len(seznam) < n:
        baza = randchoice(vse_baze)
        op = OpisBaze({
            "imena": baza.imena,
            "formula_raw": baza.formula,
            "tip_spojine": "baza",
        })
        if not ze_v_seznamu(op):
            seznam.append(op)

    return seznam


def dobi_soli(n=5, tez=1):
    return osnovni_seznam(SolniElement, SolnaIzjema, OpisSoli, n, tez)


def dobi_hidrogensoli(n=5, tez=1):
    seznam = []

    def ze_v_seznamu(opis):
        for i in seznam:
            if i == opis: return True
        return False

    elementi_1 = HidrogensolniElement.query.filter(
        HidrogensolniElement.naboj > 0
    ).all()
    elementi_2 = HidrogensolniElement.query.filter(
        HidrogensolniElement.naboj < 0
    ).all()

    while len(seznam) < n:
        el1 = randchoice(elementi_1)
        el2 = randchoice(elementi_2)
        lcm = el1.naboj * el2.naboj // gcd(el1.naboj, el2.naboj)
        n_el1 = abs(lcm // el1.naboj)
        n_el2 = abs(lcm // el2.naboj)
        stock_n = abs(el2.naboj * n_el2 // n_el1)
        data = {
            "ime1": el1.imena,
            "n1": n_el1,
            "ime2": el2.imena,
            "n2": n_el2,
            "simbol1": el1.simbol,
            "simbol2": el2.simbol,
            "stock_n": stock_n,
        }

        opis = OpisHidrogensoli(data)
        if not ze_v_seznamu(opis):
            seznam.append(opis)
            
    return seznam


def dobi_kh(n=5, tez=1):
    seznam = []

    def ze_v_seznamu(opis):
        for i in seznam:
            if i == opis: return True
        return False

    vsi_kh = Kristalohidrat.query.all()

    while len(seznam) < n:
        kh = randchoice(vsi_kh)
        op = OpisKristalohidrata({
            "imena": kh.imena,
            "formula_raw": kh.formula,
            "tip_spojine": "kristalohidrat",
        })
        if not ze_v_seznamu(op):
            seznam.append(op)
    return seznam
