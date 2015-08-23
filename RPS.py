from __future__ import generators

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

    def oppgi_navn(self):
        return self.type

class Sekvensiell:
    type = None
    last = "papir"
    lastChoice = None

    def __init__(self):
        self.type = "sekvensiell"

    def oppgi_navn(self):
        return self.type


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
    type = None
    lastChoice = None


    def __init__(self):
        self.type = "MestVanlig"

    def oppgi_navn(self):
        return self.type

    def motta_resultat(self):
        return self.lastChoice


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
        mostCommon = self.counts.index(maxN) #doesnt consider situations with several common choices
        if mostCommon == 0:
            return "papir"
        elif mostCommon == 1:
            return "stein"
        else:
            return "saks"

class Historiker:
    type = None
    husk = None
    history = []
    counts = [0, 0, 0]
    lastChoice = None

    def __init__(self, husk):
        self.type = "historiker"
        self.husk = husk

    def oppgi_navn(self):
        return self.type

    def motta_resultat(self):
        return self.lastChoice


    def addAction(self, action):
        if action == "stein":
            self.history.append(action)
        elif action == "saks":
            self.history.append(action)
        elif action == "papir":
            self.history.append(action)
        else:
            print ("Ugyldig trekk")

    def velg_aksjon(self):
        target = None
        if self.history:
            if self.husk == 1:
                target = self.history[-1]
                positions = self.get_positions(target)
                positions.pop() #removes the last position, which we dont need
                if positions:
                    for p in positions:
                        self.count(self.history[p+1])
                    maxN = max(self.counts)
                    mostCommon = self.counts.index(maxN) #doesnt consider situations with several common choices
                    if mostCommon == 0:
                        self.lastChoice = "papir"
                        return "papir"
                    elif mostCommon == 1:
                        self.lastChoice = "stein"
                        return "stein"
                    else:
                        self.lastChoice = "saks"
                        return "saks"
                else:
                    return self.counter(target)
            elif self.husk > 1:
                if len(self.history) >= self.husk:
                    return next(self.KnuthMorrisPratt(self.history, self.history[-self.husk:]))


        else:
            n = randint(0,2)
            if n == 0:
                self.lastChoice = "stein"
                return "stein"
            elif n == 1:
                self.lastChoice = "saks"
                return "saks"
            else:
                self.lastChoice = "papir"





    def get_positions(self, target):
        positions = []
        counter = 0
        for i in self.history:
            if i == target:
                positions.append(counter)
            counter = counter + 1
        return positions

    def count(self, action):
        if action == "stein":
            self.counts[0] = self.counts[0] +1
        elif action == "saks":
            self.counts[1] = self.counts[1] +1
        elif action == "papir":
            self.counts[2] = self.counts[2] +1
        else:
            print ("Ugyldig trekk")

    def counter(self, action):
        if action == "stein":
            return "papir"
        elif action == "saks":
            return "stein"
        elif action == "papir":
            return "saks"
        else:
            return "Ugyldig trekk"



        # Knuth-Morris-Pratt string matching
    # David Eppstein, UC Irvine, 1 Mar 2002



    def KnuthMorrisPratt(self, text, pattern):

        '''Yields all starting positions of copies of the pattern in the text.
    Calling conventions are similar to string.find, but its arguments can be
    lists or iterators, not just strings, it returns all matches, not just
    the first one, and it does not need the whole text in memory at once.
    Whenever it yields, it will have read the text exactly up to and including
    the match that caused the yield.'''

        # allow indexing into pattern and protect against change during yield
        pattern = list(pattern)

        # build table of shift amounts
        shifts = [1] * (len(pattern) + 1)
        shift = 1
        for pos in range(len(pattern)):
            while shift <= pos and pattern[pos] != pattern[pos-shift]:
                shift += shifts[pos-shift]
            shifts[pos+1] = shift

        # do the actual search
        startPos = 0
        matchLen = 0
        for c in text:
            while matchLen == len(pattern) or \
                  matchLen >= 0 and pattern[matchLen] != c:
                startPos += shifts[matchLen]
                matchLen -= shifts[matchLen]
            matchLen += 1
            if matchLen == len(pattern):
                yield startPos
























spiller1 = Historiker(2)
spiller2 = Tilfeldig()
print (spiller1.oppgi_navn())
print (spiller2.oppgi_navn())
print ("Tilfeldig spiller " + spiller2.velg_aksjon())
print ("Tilfeldiig spilte " + spiller2.motta_resultat())
spiller1.addAction(spiller2.motta_resultat())
print (spiller1.history)
print (spiller1.velg_aksjon())
print ("Tilfeldig spiller " + spiller2.velg_aksjon())
print ("Tilfeldiig spilte " + spiller2.motta_resultat())
spiller1.addAction(spiller2.motta_resultat())
print (spiller1.history)
print (spiller1.velg_aksjon())
print ("Tilfeldig spiller " + spiller2.velg_aksjon())
print ("Tilfeldiig spilte " + spiller2.motta_resultat())
spiller1.addAction(spiller2.motta_resultat())
print (spiller1.history)
print (spiller1.velg_aksjon())
print ("Tilfeldig spiller " + spiller2.velg_aksjon())
print ("Tilfeldiig spilte " + spiller2.motta_resultat())
spiller1.addAction(spiller2.motta_resultat())
print (spiller1.history)
print (spiller1.velg_aksjon())










