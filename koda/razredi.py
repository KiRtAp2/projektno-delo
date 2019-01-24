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
class OpisSpojine(object):

    tip_spojine = None

    def __init__(self, tip, data=None, **kwargs):
        """tip: "obicajna" / "izjema"
           če je "obicajna", daj ime1, n1, simbol1, ime2, n2, simbol2 v kwargs
           čene daj ime, ime_stock, formula_raw v kwargs
           lahko tudi daš parameter data, ki je dict iz OpisSpojine.to_dict() namesto kwargs"""
        self.tip = tip
        
        datadict = kwargs
        if data is not None:
            datadict = data
            
        if tip == "obicajna":
            self.ime1 = datadict["ime1"]
            self.n1 = int(datadict["n1"])
            self.simbol1 = datadict["simbol1"]
            self.ime2 = kwarg["ime2"]
            self.n2 = int(datadict["n2"])
            self.simbol2 = datadict["simbol2"]
        elif tip == "izjema":
            self.ime = datadict["ime"]
            self.ime_stock = datadict["ime_stock"]
            self.formula_raw = datadict["formula_raw"]
        else:
            raise ValueError("OpisSpojine(tip) dobil tip '{}', ki ni dovoljen, poglej help(razredi.OpisSpojine.__init__) za možne vrednosti")

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    def get_imena(self):
        if self.tip == "izjema":
            return self.ime, self.ime_stock

        # self.tip je zdaj "obicajna"
        st1 = STEVNIKI[self.n1]
        st2 = STEVNIKI[self.n2]

        # dodamo vsa mozna poimenovanja (trenutno s stevniki in brez)
        seznam = []
        seznam.append("{}{} {}{}".format(st1, self.ime1, st2, self.ime2))
        seznam.append("{} {}".format(self.ime1, self.ime2))

        return seznam

    def __repr__(self):
        return self.html_prikaz()

    def html_prikaz(self):
        if self.tip == "obicajna":
            s = ""
            if utils.stevilo_velikih(self.simbol1) > 1 and self.n1 > 1:
                s += "(" + self.simbol1 + ")"
            else:
                s += self.simbol1
                
            if self.n1 > 1:
                s += "<sub>{}</sub>".format(self.n1)

            if utils.stevilo_velikih(self.simbol2) > 1 and self.n2 > 1:
                s += "(" + self.simbol2 + ")"
            else:
                s += self.simbol2
            if self.n2 > 1:
                s += "<sub>{}</sub>".format(self.n2)
            return s
        
        else:
            raw1, raw2 = self.formula_raw.split("!")
            el1, *n1 = raw1.split("_")
            n1 = 1 if len(n1) == 0 else int(n1[0])
            el2, *n2 = raw2.split("_")
            n2 = 1 if len(n2) == 0 else int(n2[0])

            s = ""
            s += el1
            if n1 > 1:
                s += "<sub>{}</sub>".format(n1)
            s += el2
            if n2 > 1:
                s += "<sub>{}</sub>".format(n2)

            return s

    def to_dict(self):
        if self.tip == "obicajna":
            d = {
                "ime1": self.ime1,
                "n1": self.n1,
                "simbol1": self.simbol1,
                "ime2": self.ime2,
                "n2": self.n2,
                "simbol2": self.simbol2
            }
        else:
            d = {
                "ime": self.ime,
                "ime_stock": self.ime_stock,
                "formula_raw": self.formula_raw
            }
        return d.update({
            "tip": self.tip,
            "tip_spojine": self.tip_spojine
        })

    def to_json(self):
        return json.dumps(self.to_dict())

    
class OpisBinarne(OpisSpojine):
    tip_spojine = "binarna"

    
class SolnaSpojina(NekaSpojina):
    def get_sp_type(self):
        return "Sol"

class BinarnaSpojina(NekaSpojina):
    def get_sp_type(self):
        return "binarna"


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


def konstruiraj(d: dict):
    """Konstruiraj spojino iz dict objekta. Vrne Opis neke spojine"""
    if d["tip_spojine"] == "binarna":
        return OpisBinarne(d)
    else:
        return ValueError("tip_spojine ({}) ni prepoznan".format(d["tip_spojine"]))
    
