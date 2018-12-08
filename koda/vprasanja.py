u"""Datoteka vsebuje osnovne funkcije za postavljanje in preverjanje vprašanj"""


from random import choice as randchoice
from math import gcd

from models import BinarniElement, BazniElement, KisliElement, SolniElement
from razredi import BinarnaSpojina, BaznaSpojina, KislaSpojina, SolnaSpojina


def osnovni_seznam(tip_element, tip_spojina, n=5):
    seznam = []

    def ze_v_seznamu(spojina):
        for i in seznam:
            if i == spojina:
                return True
        return False

    elementi_1 = tip_element.query.filter(
        tip_element.naboj > 0
    ).all()

    elementi_2 = tip_element.query.filter(
        tip_element.naboj < 0
    ).all()

    while len(seznam) < n:

        el1 = randchoice(elementi_1)
        el2 = randchoice(elementi_2)

        lcm = el1.naboj * el2.naboj / gcd(el1.naboj, el2.naboj)

        n_el1 = lcm // el1.naboj
        n_el2 = lcm // el2.naboj

        sp = tip_spojina(el1, abs(n_el1), el2, abs(n_el2))
        if not ze_v_seznamu(sp):
            seznam.append(sp)
        
    return seznam


def dobi_binarne(n=5):
    return osnovni_seznam(BinarniElement, BinarnaSpojina, n)


def dobi_baze(n=5):
    return osnovni_seznam(BazniElement, BaznaSpojina, n)


def dobi_kisline(n=5):
    return osnovni_seznam(KisliElement, KislaSpojina, n)


def dobi_soli(n=5):
    return osnovni_seznam(SolniElement, SolnaSpojina, n)


def dobi_kh(n=5):
    pass


