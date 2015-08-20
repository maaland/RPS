__author__ = 'Marius'

from random import randint



class Tilfeldig:

    type = None
    last = "papir"
    lastChoice = None

    def __init__(self):
            self.type = "tilfeldig"



    def velg_aksjon(self):
        if self.type == "tilfeldig":
            n = randint(0,2)
            if n == 0:
                self.lastChoice = "stein"
                return "stein"
            elif n == 1:
                self.lastChoice = "saks"
                return "saks"
            else:
                self.lastChoice = "papir"
                return "papir"


    def motta_resultat(self):
        return self.lastChoice

class Sekvensiell:
    last = "papir"

    def velg_aksjon(self):
        next = None
        if self.last == "stein":
            next = "saks"
        elif self.last == "saks":
            next = "papir"
        elif self.last == "papir":
            next = "stein"
        else:
            print ("Ugyldig trekk")
        self.last = next
        self.lastChoice = next
        return next












spiller1 = Sekvensiell()
print (spiller1.velg_aksjon())
print (spiller1.velg_aksjon())
print (spiller1.velg_aksjon())
print (spiller1.velg_aksjon())
print (spiller1.velg_aksjon())
print (spiller1.velg_aksjon())
print (spiller1.velg_aksjon())
print (spiller1.velg_aksjon())
print (spiller1.velg_aksjon())



