import json
import string

import utils


STEVNIKI = {
    0: "",
    1: "",
    2: "di",
    3: "tri",
    4: "tetra",
    5: "penta",
    6: "heksa",
    7: "hepta",
    8: "okta",
    9: "nona",
    10: "deka"
}


def imena(el1, el2, n1, n2, brez_stevnikov=True, stock=True):
    return NekaSpojina(el1, n1, el2, n2).get_imena(brez_stevnikov, stock)


class NekaSpojina(object):

    def __init__(self, el1, n1, el2, n2):
        self.el1, self.n1, self.el2, self.n2 = el1, n1, el2, n2

    def __eq__(self, other):
        return self.el1 == other.el1 and self.el2 == other.el2

    @property
    def formula(self):
        return self.el1, self.n1, self.el2, self.n2

    def get_imena(self, brez_stevnikov=True, stock=True):
        stevnik = lambda x: STEVNIKI[x]

        st1 = stevnik(self.n1)
        st2 = stevnik(self.n2)

        ime1 = self.el1 if type(self.el1) == str else self.el1.ime
        ime2 = self.el2 if type(self.el2) == str else self.el2.ime

        seznam = []
        seznam.append("{}{} {}{}".format(st1, ime1, st2, ime2))

        if brez_stevnikov:
            seznam.append("{} {}".format(ime1, ime2))

        return seznam

    def __repr__(self):
        s = ""
        if utils.stevilo_velikih(self.el1.simbol) > 1 and self.n1 > 1:
            s += "(" + self.el1.simbol + ")"
        else:
            s += self.el1.simbol
            
        if self.n1 > 1:
            s += "<sub>{}</sub>".format(int(self.n1))

        if utils.stevilo_velikih(self.el2.simbol) > 1 and self.n2 > 1:
            s += "(" + self.el2.simbol + ")"
        else:
            s += self.el2.simbol
            
        if self.n2 > 1:
            s += "<sub>{}</sub>".format(int(self.n2))

        return s

    def get_sp_type(self):
        return None
    
    def to_dict(self):
        d = {
            "type": self.get_sp_type(),
            "html_formula": self.__repr__(),
            "1": {
                "count": self.n1,
                "simbol": self.el1.ime,
            },
            "2": {
                "count": self.n2,
                "simbol": self.el2.ime,
            }
        }
        return d
    
    def to_json(self):
        return json.dumps(self.to_dict())

    
class BinarnaSpojina(NekaSpojina):
    def get_sp_type(self):
        return "BinarnaSpojina"

    
class BaznaSpojina(NekaSpojina):
    def get_sp_type(self):
        return "Baza"

    
class KislaSpojina(NekaSpojina):
    def get_sp_type(self):
        return "Kislina"

    
class SolnaSpojina(NekaSpojina):
    def get_sp_type(self):
        return "Sol"


class SpojinaIzjema(NekaSpojina):

    def __init__(self, formula: str, ime: str, ime_stock: str):
        self.formula_raw = formula
        self.ime = ime
        self.ime_stock = ime_stock

    def __eq__(self, other):
        return self.formula == other.formula

    @property
    def formula(self):
        dela = self.formula_raw.split("!")
        print(self.formula_raw, dela)
        el1, *n1 = dela[0].split("_")
        if len(n1) == 0:
            n1 = 0
        else:
            n1 = int(n1[0])

        el2, *n2 = dela[1].split("_")
        if len(n2) == 0:
            n2 = 0
        else:
            n2 = int(n2[0])

        return el1, n1, el2, n2

    def get_imena(self, brez_stevnikov=True, stock=True):
        return [self.ime, self.ime_stock]

    def __repr__(self):
        el1, n1, el2, n2 = self.formula
        s = ""
        if utils.stevilo_velikih(el1) > 1 and n1 > 1:
            s += "(" + el1 + ")"
        else:
            s += el1
            
        if n1 > 1:
            s += "<sub>{}</sub>".format(n1)

        if utils.stevilo_velikih(el2) > 1 and n2 > 1:
            s += "(" + el2 + ")"
        else:
            s += el2
            
        if n2 > 1:
            s += "<sub>{}</sub>".format(n2)

        return s

    def get_sp_type(self):
        return "izjema"

    def to_dict(self):
        el1, n1, el2, n2 = self.formula
        d = {
            "type": self.get_sp_type(),
            "html_formula": self.__repr__(),
            "1": {
                "count": n1,
                "simbol": el1
            },
            "2": {
                "count": n2,
                "simbol": el2
            }
        }
        return d
    
