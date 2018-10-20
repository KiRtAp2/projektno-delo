u"""Datoteka vsebuje osnovne funkcije za postavljanje in preverjanje vprašanj"""


from random import choice as randchoice
from math import gcd

from models import BinarniElement
from razredi import BinarnaSpojina


def dobi_binarne():

    seznam = []

    while len(seznam) < 5:

        el1 = randchoice(BinarniElement.query.filter(
            BinarniElement.naboj > 0
        ).all())
        el2 = randchoice(BinarniElement.query.filter(
            BinarniElement.naboj < 0
        ).all())

        lcm = el1.naboj * el2.naboj / gcd(el1.naboj, el2.naboj)

        n_el1 = lcm / el1.naboj
        n_el2 = lcm / el2.naboj

        seznam.append(
            BinarnaSpojina(el1, n_el1, el2, n_el2)
        )
        
    return seznam



# napisi mi tukaj funkcije ki jih zelis videti
# recimo:
# def dobi_nekej(n: int=3):
#     pass

def dobi_bazo(): #n = 5 lahko das kr notr v funkcijo ker se n nebo spreminju
    pass

def dobi_kislino():
    pass

def dobi_kh():
    pass

def dobi_sol():
    pass
