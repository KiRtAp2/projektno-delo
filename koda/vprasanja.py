u"""Datoteka vsebuje osnovne funkcije za postavljanje in preverjanje vprašanj"""


from random import choice as randchoice
from math import gcd

from models import BinarniElement, BazniElement, KisliElement, SolniElement
from razredi import BinarnaSpojina, BaznaSpojina, KislaSpojina, SolnaSpojina


def osnovni_seznam(tip_element, tip_spojina, n=5):
    seznam = []

    while len(seznam) < n:

        el1 = randchoice(tip_element.query.filter(
            tip_element.naboj > 0
        ).all())
        el2 = randchoice(tip_element.query.filter(
            tip_element.naboj < 0
        ).all())

        lcm = el1.naboj * el2.naboj / gcd(el1.naboj, el2.naboj)

        n_el1 = lcm // el1.naboj
        n_el2 = lcm // el2.naboj

        seznam.append(
            tip_spojina(el1, abs(n_el1), el2, abs(n_el2))
        )
        
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


