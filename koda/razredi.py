import json


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

def ime(el1, el2, n1, n2):
    stevnik = lambda x: STEVNIKI[x]
        
    st1 = stevnik(n1)
    st2 = stevnik(n2)

    ime1 = el1
    ime2 = el2

    return "{}{} {}{}".format(
        st1, ime1, st2, ime2
    )


class NekaSpojina(object):

    def __init__(self, el1, n1, el2, n2):
        self.el1, self.n1, self.el2, self.n2 = el1, n1, el2, n2

    @property
    def formula(self):
        return self.el1, self.n1, self.el2, self.n2

    def get_ime(self):
        stevnik = lambda x: STEVNIKI[x]
        
        st1 = stevnik(self.n1)
        st2 = stevnik(self.n2)

        ime1 = self.el1.ime
        ime2 = self.el2.ime

        return "{}{} {}{}".format(
            st1, ime1, st2, ime2
        )

    def __repr__(self):
        s = ""
        s += self.el1.simbol
        if self.n1 > 1:
            s += "<sub>{}</sub>".format(int(self.n1))

        s += self.el2.simbol
        if self.n2 > 1:
            s += "<sub>{}</sub>".format(int(self.n2))

        return s

    def get_sp_type(self):
        return None
    
    def to_dict(self):
        d = {
            "type": self.get_sp_type(),
            "formula": self.__repr__(),
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

