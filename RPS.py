__author__ = 'Marius'

from random import randint



class Spiller:

    type = None
    last = "papir"

    def __init__(self, type):
        if type == "tilfeldig":
            self.type = type
        elif type == "sekvensiell":
            self.type = type
        elif type == "mestvanlig":
            self.type = type
        elif type == "historiker":
            self.type = type
        else:
            print ("Ugyldig typevalg")


    def velg_aksjon(self):
        if self.type == "tilfeldig":
            n = randint(0,2)
            if n == 0:
                return "stein"
            elif n == 1:
                return "saks"
            else:
                return "papir"
        elif self.type == "sekvensiell":

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
            return next













spiller1 = Spiller("sekvensiell")
print (spiller1.velg_aksjon())
print (spiller1.velg_aksjon())
print (spiller1.velg_aksjon())
print (spiller1.velg_aksjon())
print (spiller1.velg_aksjon())
print (spiller1.velg_aksjon())
print (spiller1.velg_aksjon())
print (spiller1.velg_aksjon())
print (spiller1.velg_aksjon())



