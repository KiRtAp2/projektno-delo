class BinarnaSpojina(object):

    def __init__(self, el1, n1, el2, n2):
        self.el1, self.n1, self.el2, self.n2 = el1, n1, el2, n2

    @property
    def formula(self):
        return self.el1, self.n1, self.el2, self.n2

    def get_ime(self):
        stevnik = lambda x: {  # to je switch v pythonu
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
        }[x]
        
        st1 = stevnik(abs(self.n1))
        st2 = stevnik(abs(self.n2))

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

    # tole prosim dodej
    def to_json(self):
        pass
