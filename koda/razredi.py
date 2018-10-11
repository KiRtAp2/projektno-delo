class BinarnaSpojina(object):

    def __init__(self, el1, n1, el2, n2):
        self.el1, self.n1, self.el2, self.n2 = el1, n1, el2, n2

    @property
    def formula(self):
        return self.el1, self.n1, self.el2, self.n2

    def get_ime(self):
        stevnik1 = (lambda x: {  # to je switch v pythonu
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
        }[x])(self.n1)

        stevnik2 = (lambda x: {  # to je switch v pythonu
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
        }[x])(self.n2)

        ime1 = self.el1.ime
        ime2 = self.el2.ime

        return "{}{}{}{}".format(
            stevnik1, ime1, stevnik2, ime2
        )
