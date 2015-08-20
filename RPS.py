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
    type = None
    last = "papir"
    lastChoice = None

    def __init__(self):
        self.type = "tilfeldig"


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

    def motta_resultat(self):
        return self.lastChoice

class MestVanlig:
    counts = [0, 0, 0]


    def __init__(self):
        self.type = "MestVanlig"


    def addAction(self, action):
        if action == "stein":
            self.counts[0] = self.counts[0] +1
        elif action == "saks":
            self.counts[1] = self.counts[1] +1
        elif action == "papir":
            self.counts[2] = self.counts[2] +1
        else:
            print ("Ugyldig trekk")

    def velg_aksjon(self):
        maxN = max(self.counts)
        if maxN == 0:
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
        mostCommon = self.counts.index(maxN)
        if mostCommon == 0:
            return "papir"
        elif mostCommon == 1:
            return "stein"
        else:
            return "saks"
















spiller1 = MestVanlig()
spiller2 = Sekvensiell()
spiller2.velg_aksjon()
print (spiller2.motta_resultat())
spiller1.addAction(spiller2.motta_resultat())
print (spiller1.counts)
print (spiller1.velg_aksjon())






