import json
import string

import utils


PREPOVEDANI_STOCK = {
    "NH4",
    "Li",
    "Be",
    "Na",
    "Mg",
    "K",
    "Ca",
    "Rb",
    "Sr",
    "Cs",
    "Ba",
    "Al",
}

PREPOVEDANA_IMENA = {
    "silicijev dioksid",
}

STEVNIKI = {
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

RIMSKI = [
    "Nekaj je šlo hudo narobe...",
    "I",
    "II",
    "III",
    "IV",
    "V",
    "VI",
    "VII",
    "VIII"
]


def prikaz_skupine(s: str, formatiraj=True):
    final = ""
    velika_cifra = False
    for ch in s:
        if ch in string.digits:
            if velika_cifra or not formatiraj: final += ch
            else: final += "<sub>{}</sub>".format(ch)
        elif ch == "*":
            if not formatiraj: final += "*"
            else:
                final += " &#x00B7 "
                velika_cifra = True
        else:
            final += ch
            velika_cifra = False
    return final


class OpisSpojine(object):

    tip_spojine = None
    imenovanja = []

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
            self.ime2 = datadict["ime2"]
            self.n2 = int(datadict["n2"])
            self.simbol2 = datadict["simbol2"]
            self.stock_n = datadict["stock_n"]
        elif tip == "izjema":
            self.imena = datadict["imena"]
            self.formula_raw = datadict["formula_raw"]
        else:
            raise ValueError("OpisSpojine(tip) dobil tip '{}', ki ni dovoljen, poglej help(razredi.OpisSpojine.__init__) za možne vrednosti".format(tip))

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    def get_imena(self):
        if self.tip == "izjema":
            return self.imena.split("=")

        # self.tip je zdaj "obicajna"
        st1 = STEVNIKI[self.n1]
        st2 = STEVNIKI[self.n2]

        seznam = []
        
        for ime1 in self.ime1.split("="):
            for ime2 in self.ime2.split("="):
                # dodamo vsa mozna poimenovanja
                if "stevniki" in self.imenovanja: seznam.append("{}{} {}{}".format(st1, ime1, st2, ime2))
                if "brez" in self.imenovanja: seznam.append("{} {}".format(ime1, ime2))
                if self.stock_n != 0 and "stock" in self.imenovanja and self.simbol1 not in PREPOVEDANI_STOCK and self.simbol2 not in PREPOVEDANI_STOCK:
                    # self.stock_n je nastavljen na 0, če se spojine ne da opisati s stockom
                    seznam.append("{el1}({n}) {el2}".format(el1=ime1, el2=ime2, n=RIMSKI[self.stock_n]))

        for i in seznam:
            if i in PREPOVEDANA_IMENA:
                seznam.remove(i)

        return seznam

    def __repr__(self):
        return self.html_prikaz(True)

    def html_prikaz(self, formatiranje=True):
        if self.tip == "obicajna":
            s1 = prikaz_skupine(self.simbol1, formatiranje)
            s2 = prikaz_skupine(self.simbol2, formatiranje)

            if self.n1 > 1:
                if utils.stevilo_velikih(s1) > 1:
                    if formatiranje:
                        s1 = "({})<sub>{}</sub>".format(s1, self.n1)
                    else:
                        s1 = "({}){}".format(s1, self.n1)
                else:
                    if formatiranje:
                        s1 = "{}<sub>{}</sub>".format(s1, self.n1)
                    else:
                        s1 = "{}{}".format(s1, self.n1)

            if self.n2 > 1:
                if utils.stevilo_velikih(s2) > 1:
                    if formatiranje:
                        s2 = "({})<sub>{}</sub>".format(s2, self.n2)
                    else:
                        s2 = "({}){}".format(s2, self.n2)
                else:
                    if formatiranje:
                        s2 = "{}<sub>{}</sub>".format(s2, self.n2)
                    else:
                        s2 = "{}{}".format(s2, self.n2)
            return s1+s2
        else:
            return prikaz_skupine(self.formula_raw, formatiranje)

    def to_dict(self):
        if self.tip == "obicajna":
            d = {
                "ime1": self.ime1,
                "n1": self.n1,
                "simbol1": self.simbol1,
                "ime2": self.ime2,
                "n2": self.n2,
                "simbol2": self.simbol2,
                "stock_n": self.stock_n,
                "imenovanja": self.imenovanja,
            }
        else:
            d = {
                "imena": self.imena,
                "formula_raw": self.formula_raw
            }
        d.update({
            "tip": self.tip,
            "tip_spojine": self.tip_spojine
        })
        return d

    def to_json(self):
        return json.dumps(self.to_dict())


class AbstractOpisElementarne(OpisSpojine):
    tip_spojine = None
    imenovanja = None

    def __init__(self, data=None, **kwargs):
        if data is None:
            datadict = kwargs
        else:
            datadict = data

        self.ime1 = datadict["ime1"]
        self.n1 = int(datadict["n1"])
        self.simbol1 = datadict["simbol1"]
        self.ime2 = datadict["ime2"]
        self.n2 = int(datadict["n2"])
        self.simbol2 = datadict["simbol2"]
        self.stock_n = datadict["stock_n"]

    def get_imena(self):
        st1 = STEVNIKI[self.n1]
        st2 = STEVNIKI[self.n2]

        seznam = []

        for ime1 in self.ime1.split("="):
            for ime2 in self.ime2.split("="):
                if "stevniki" in self.imenovanja: seznam.append("{}{} {}{}".format(st1, ime1, st2, ime2))
                if "brez" in self.imenovanja: seznam.append("{} {}".format(ime1, ime2))
                if self.stock_n != 0 and "stock" in self.imenovanja:
                    seznam.append("{el1}({n}) {el2}".format(el1=ime1, el2=ime2, n=RIMSKI[self.stock_n]))

        for i in seznam:
            if i in PREPOVEDANA_IMENA:
                seznam.remove(i)
                    
        return seznam

    def html_prikaz(self, formatiranje=True):
        s1 = prikaz_skupine(self.simbol1, formatiranje)
        s2 = prikaz_skupine(self.simbol2, formatiranje)

        if self.n1 > 1:
            if utils.stevilo_velikih(s1) > 1:
                if formatiranje:
                    s1 = "({})<sub>{}</sub>".format(s1, self.n1)
                else:
                    s1 = "({}){}".format(s1, self.n1)
            else:
                if formatiranje:
                    s1 = "{}<sub>{}</sub>".format(s1, self.n1)
                else:
                    s1 = "{}{}".format(s1, self.n1)

        if self.n2 > 1:
            if utils.stevilo_velikih(s2) > 1:
                if formatiranje:
                    s2 = "({})<sub>{}</sub>".format(s2, self.n2)
                else:
                    s2 = "({}){}".format(s2, self.n2)
            else:
                if formatiranje:
                    s2 = "{}<sub>{}</sub>".format(s2, self.n2)
                else:
                    s2 = "{}{}".format(s2, self.n2)
        return s1+s2

    def to_dict(self):
        d = {
            "ime1": self.ime1,
            "n1": self.n1,
            "simbol1": self.simbol1,
            "ime2": self.ime2,
            "n2": self.n2,
            "simbol2": self.simbol2,
            "stock_n": self.stock_n,
            "tip_spojine": self.tip_spojine,
            "imenovanja": self.imenovanja,
        }
        return d

    
class AbstractOpisIzjeme(OpisSpojine):
    tip_spojine = None

    def __init__(self, data=None, **kwargs):
        if data is None:
            datadict = kwargs
        else:
            datadict = data

        self.imena = datadict["imena"].split("=")
        self.formula_raw = datadict["formula_raw"]
        
    def get_imena(self):
        return self.imena

    def html_prikaz(self, formatiranje):
        prikaz = prikaz_skupine(self.formula_raw, formatiranje)
        return prikaz

    def to_dict(self):
        return {
            "tip_spojine": self.tip_spojine,
            "imena": "=".join(self.imena),
            "formula_raw": self.formula_raw,
        }
    

class OpisBinarne(OpisSpojine):
    tip_spojine = "binarna"
    imenovanja = ["stevniki", "brez", "stock"]

    
class OpisKisline(AbstractOpisIzjeme):
    tip_spojine = "kislina"

    
class OpisBaze(AbstractOpisIzjeme):
    tip_spojine = "baza"

    
class OpisSoli(OpisSpojine):
    tip_spojine = "sol"
    imenovanja =  ["brez", "stock"]

    
class OpisHidrogensoli(AbstractOpisElementarne):
    tip_spojine = "hidrogensol"
    imenovanja = ["brez", "stock"]


class OpisKristalohidrata(AbstractOpisIzjeme):
    tip_spojine = "kristalohidrat"


def konstruiraj(d: dict):
    """Konstruiraj spojino iz dict objekta. Vrne Opis neke spojine"""
    if d["tip_spojine"] == "binarna":
        return OpisBinarne(d["tip"], d)
    elif d["tip_spojine"] == "kislina":
        return OpisKisline(d)
    elif d["tip_spojine"] == "baza":
        return OpisBaze(d)
    elif d["tip_spojine"] == "sol":
        return OpisSoli(d["tip"], d)
    elif d["tip_spojine"] == "hidrogensol":
        return OpisHidrogensoli(d)
    elif d["tip_spojine"] == "kristalohidrat":
        return OpisKristalohidrata(d)
    else:
        return ValueError("tip_spojine ({}) ni prepoznan".format(d["tip_spojine"]))
