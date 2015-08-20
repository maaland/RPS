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
    rocks = 0
    papers = 0
    scissors = 0


    def __init__(self):
        self.type = "MestVanlig"


    def addAction(self, action):
        if action == "stein":
            self.rocks = self.rocks + 1
        elif action == "saks":
            self.scissors = self.scissors + 1
        elif action == "papir":
            self.paper = self.paper + 1
        else:
            print ("Ugyldig trekk")













spiller1 = MestVanlig()
spiller2 = Sekvensiell()
spiller2.velg_aksjon()
print (spiller2.motta_resultat())
spiller1.addAction(spiller2.motta_resultat())
print (spiller1.rocks)
print (spiller1.papers)
print (spiller1.scissors)






