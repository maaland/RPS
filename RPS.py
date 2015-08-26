from __future__ import generators

__author__ = 'Marius'

from random import randint

# Import statements
# Disse brukes for å hente inn pakker til programmet vårt.
# Beskrivelse på wiki om hvordan disse installeres på maskinen og gjøres tilgjengelig
from tkinter import Tk, BOTH, StringVar
from tkinter.ttk import Frame, Button, Label, Style
import pylab
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy


class Aksjon:
    action = None

    def __init__(self, action):
        self.action = action

    def __eq__(self, other):
        return other.action == self.action

    def __gt__(self, other):
        if self.action.lower() == "stein":
            return other.action == "saks"
        elif self.action.lower() == "saks":
            return other.action == "papir"
        elif self.action.lower() == "papir":
            return other.action == "stein"
        else:
            return "gt: Ugyldig trekk"


class Tilfeldig:
    type = None
    lastChoice = None

    def __init__(self):
        self.type = "tilfeldig"

    def velg_aksjon(self):

        n = randint(0, 2)
        if n == 0:
            self.lastChoice = Aksjon("stein")
            return self.lastChoice
        elif n == 1:
            self.lastChoice = Aksjon("saks")
            return self.lastChoice
        else:
            self.lastChoice = Aksjon("papir")
            return self.lastChoice

    def motta_resultat(self):
        return self.lastChoice

    def oppgi_navn(self):
        return self.type


class Sekvensiell:
    type = None
    lastChoice = None

    def __init__(self):
        self.type = "sekvensiell"

    def oppgi_navn(self):
        return self.type

    def velg_aksjon(self):
        next = None
        if not self.lastChoice:
            next = Aksjon("stein")
        elif self.lastChoice.action.lower() == "stein":
            next = Aksjon("saks")
        elif self.lastChoice.action.lower() == "saks":
            next = Aksjon("papir")
        elif self.lastChoice.action.lower() == "papir":
            next = Aksjon("stein")

        else:
            print("velg_aksjon: Ugyldig trekk")
        self.lastChoice = next
        return self.lastChoice

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
        if action.action.lower() == "stein":
            self.counts[0] = self.counts[0] + 1
        elif action.action.lower() == "saks":
            self.counts[1] = self.counts[1] + 1
        elif action.action.lower() == "papir":
            self.counts[2] = self.counts[2] + 1
        else:
            print("Ugyldig trekk")

    def velg_aksjon(self):
        maxN = max(self.counts)
        if maxN == 0:
            n = randint(0, 2)
            if n == 0:
                self.lastChoice = Aksjon("stein")
                return self.lastChoice
            elif n == 1:
                self.lastChoice = Aksjon("saks")
                return self.lastChoice
            else:
                self.lastChoice = Aksjon("papir")
                return self.lastChoice
        mostCommon = self.counts.index(maxN)  # doesnt consider situations with several common choices
        if mostCommon == 0:
            return Aksjon("papir")
        elif mostCommon == 1:
            return Aksjon("stein")
        else:
            return Aksjon("saks")


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
        if action.action.lower() == "stein":
            self.history.append(action)
        elif action.action.lower() == "saks":
            self.history.append(action)
        elif action.action.lower() == "papir":
            self.history.append(action)
        else:
            print("Ugyldig trekk")


    def velg_aksjon(self):
        target = None
        if self.history:
            if int(self.husk) == 1:
                target = self.history[-1]
                positions = self.get_positions(target)
                positions.pop()  # removes the last position, which we dont need
                if positions:
                    for p in positions:
                        self.count(self.history[p + 1])  # counts up the actions follow the pattern
                    maxN = max(self.counts)
                    mostCommon = self.counts.index(maxN)  # doesnt consider situations with several common choices
                    if mostCommon == 0:
                        self.lastChoice = Aksjon("papir")
                        return self.lastChoice
                    elif mostCommon == 1:
                        self.lastChoice = Aksjon("stein")
                        return self.lastChoice
                    else:
                        self.lastChoice = Aksjon("saks")
                        return self.lastChoice
                else:
                    return self.counter(target)
            elif int(self.husk) > 1:
                if len(self.history) >= int(self.husk):
                    positions = []
                    for pos in self.KnuthMorrisPratt(self.history, self.history[
                                                                   -int(self.husk):]):  # iterates through the occurances of the husk-last actions
                        if pos + int(self.husk) < len(self.history) - 1:  # filters out the last occurance
                            positions.append(pos)  # adds the positions of the occurances to a list
                    if positions:
                        for p in positions:
                            self.count(self.history[p + int(self.husk)])  # counts up the actions follow the pattern
                        maxN = max(self.counts)
                        mostCommon = self.counts.index(maxN)  # doesnt consider situations with several common choices
                        if mostCommon == 0:
                            self.lastChoice = Aksjon("papir")
                            return self.lastChoice
                        elif mostCommon == 1:
                            self.lastChoice = Aksjon("stein")
                            return self.lastChoice
                        else:
                            self.lastChoice = Aksjon("saks")
                            return self.lastChoice
                    else:
                        return self.randomAction()  # random if the pattern is not found
                else:
                    return self.randomAction()  # random if the pattern is longer than the history
        else:
            return self.randomAction()

    def get_positions(self, target):  # helper function to add targets positions to a list
        positions = []
        counter = 0
        for i in self.history:
            if i == target:
                positions.append(counter)
            counter = counter + 1
        return positions

    def count(self, action):  # helper function to count actions
        if action.action.lower() == "stein":
            self.counts[0] = self.counts[0] + 1
        elif action.action.lower() == "saks":
            self.counts[1] = self.counts[1] + 1
        elif action.action.lower() == "papir":
            self.counts[2] = self.counts[2] + 1
        else:
            print("count: ugyldig trekk")

    def counter(self, action):  # helper function to choose a counter for an action
        if action.action.lower() == "stein":
            return Aksjon("papir")
        elif action.action.lower() == "saks":
            return Aksjon("stein")
        elif action.action.lower() == "papir":
            return Aksjon("saks")
        else:
            return "counter: Ugyldig trekk"

    def randomAction(self):  # helper function to choose a random action
        n = randint(0, 2)
        if n == 0:
            self.lastChoice = Aksjon("stein")
            return self.lastChoice
        elif n == 1:
            self.lastChoice = Aksjon("saks")
            return self.lastChoice
        else:
            self.lastChoice = Aksjon("papir")
            return self.lastChoice



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
            while shift <= pos and pattern[pos] != pattern[pos - shift]:
                shift += shifts[pos - shift]
            shifts[pos + 1] = shift

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


class EnkeltSpill:
    resultat = [0, 0]
    choices = []
    winner = [0]


    def __init__(self, spiller1, spiller2):
        if spiller1 == "tilfeldig":
            self.spiller1 = Tilfeldig()
        elif spiller1 == "sekvensiell":
            self.spiller1 = Sekvensiell()
        elif spiller1 == "mestvanlig":
            self.spiller1 = MestVanlig()
        elif spiller1 == "historiker":
            husk = input("Husk: ")
            if int(husk) > 0:
                self.spiller1 = Historiker(husk)

        if spiller2 == "tilfeldig":
            self.spiller2 = Tilfeldig()
        elif spiller2 == "sekvensiell":
            self.spiller2 = Sekvensiell()
        elif spiller2 == "mestvanlig":
            self.spiller2 = MestVanlig()
        elif spiller2 == "historiker":
            husk = input("Husk: ")  # requires input to determine husk value
            if int(husk) > 0:
                self.spiller2 = Historiker(husk)



    def gjennomfoer_spill(self):
        spiller1aksjon = self.spiller1.velg_aksjon()
        spiller2aksjon = self.spiller2.velg_aksjon()
        if isinstance(self.spiller1, MestVanlig) or isinstance(self.spiller1, Historiker):  # adds p2's action if p1 wants it
            self.spiller1.addAction(spiller2aksjon)
        elif self.spiller2.oppgi_navn() == "mestvanlig" or self.spiller2.oppgi_navn() == "historiker":  # adds p1's action if p2 wants it
            self.spiller2.addAction(spiller1aksjon)
        self.choices.append(spiller1aksjon.action)  # add the chosen action to choices
        self.choices.append(spiller2aksjon.action)
        if spiller1aksjon.__gt__(spiller2aksjon):  # if player 1 wins, add 1 point
            self.resultat[0] = self.resultat[0] + 1
            self.winner[0] = 1
        elif spiller1aksjon.__eq__(spiller2aksjon):  # if tie, add 0.5 points to both
            self.resultat[0] = self.resultat[0] + 0.5
            self.resultat[1] = self.resultat[1] + 0.5
            self.winner[0] = 0
        else:
            self.resultat[1] = self.resultat[1] + 1  # player 2 wins, add 1 point
            self.winner[0] = 2

        return (spiller1aksjon.action, spiller2aksjon.action, self.resultat)

    def __str__(self):
        res = "{}: {}, {}: {} ".format(self.spiller1.oppgi_navn(), self.choices[-2], self.spiller2.oppgi_navn(), self.choices[-1])
        if self.winner[0] == 1:
            res = res + "og {} vant".format(self.spiller1.oppgi_navn())
        elif self.winner[0] == 2:
            res = res + "og {} vant".format(self.spiller2.oppgi_navn())
        elif self.winner[0] == 0:
            res = res + "og det ble uavgjort"

        return res


class MangeSpill:




    def __init__(self, spiller1, spiller2, antall_spill):
        self.antall_spill = antall_spill
        self.enkeltSpill = EnkeltSpill(spiller1, spiller2)
        self.spiller1 = self.enkeltSpill.spiller1
        self.spiller2 = self.enkeltSpill.spiller2

    def arranger_enkeltspill(self):
        return self.enkeltSpill.gjennomfoer_spill()

    def arranger_turnering(self):
        spilt = 0
        pros1 = 0
        pros2 = 0
        turneringspill = None
        while spilt <= self.antall_spill:
            turneringspill = self.arranger_enkeltspill()
            spilt = spilt + 1
        if turneringspill:
            pros1 = (turneringspill[2][0] / sum(turneringspill[2])) * 100
            pros2 = (turneringspill[2][1] / sum(turneringspill[2])) * 100
        return pros1, pros2

    def __str__(self):
        return self.enkeltSpill.__str__()







'''spiller1 = Historiker(2)
spiller2 = Tilfeldig()
print (spiller1.oppgi_navn())
print (spiller2.oppgi_navn())
print ("Tilfeldig spiller " + spiller2.velg_aksjon().action)
print ("Tilfeldiig spilte " + spiller2.motta_resultat().action)
spiller1.addAction(spiller2.motta_resultat())
printhistory = []
for a in spiller1.history:
    printhistory.append(a.action)
print(printhistory)
print (spiller1.velg_aksjon.action)
print ("Tilfeldig spiller " + spiller2.velg_aksjon().action)
print ("Tilfeldiig spilte " + spiller2.motta_resultat().action)
spiller1.addAction(spiller2.motta_resultat())
printhistory = []
for a in spiller1.history:
    printhistory.append(a.action)
print(printhistory)
print (spiller1.velg_aksjon.action)
print ("Tilfeldig spiller " + spiller2.velg_aksjon().action)
print ("Tilfeldiig spilte " + spiller2.motta_resultat().action)
spiller1.addAction(spiller2.motta_resultat())
printhistory = []
for a in spiller1.history:
    printhistory.append(a.action)
print(printhistory)
print (spiller1.velg_aksjon.action)
print ("Tilfeldig spiller " + spiller2.velg_aksjon().action)
print ("Tilfeldiig spilte " + spiller2.motta_resultat().action)
spiller1.addAction(spiller2.motta_resultat())
printhistory = []
for a in spiller1.history:
    printhistory.append(a.action)
print(printhistory)
print (spiller1.velg_aksjon.action)
print ("Tilfeldig spiller " + spiller2.velg_aksjon().action)
print ("Tilfeldiig spilte " + spiller2.motta_resultat().action)
spiller1.addAction(spiller2.motta_resultat())
printhistory = []
for a in spiller1.history:
    printhistory.append(a.action)
print(printhistory)
print (spiller1.velg_aksjon.action)
print ("Tilfeldig spiller " + spiller2.velg_aksjon().action)
print ("Tilfeldiig spilte " + spiller2.motta_resultat().action)
spiller1.addAction(spiller2.motta_resultat())
printhistory = []
for a in spiller1.history:
    printhistory.append(a.action)
print(printhistory)
print (spiller1.velg_aksjon.action)
'''

'''action1 = Aksjon("stein")
action2 = Aksjon("stein")
action3 = Aksjon("papir")
print (action1.__eq__(action2))
print (action1.__gt__(action2))
print (action3.__gt__(action1))
print (action3.__eq__(action1))'''
'''spill = MangeSpill("historiker", "sekvensiell", 100)
print(spill.spiller1.oppgi_navn())
print(spill.spiller2.oppgi_navn())
print(spill.arranger_turnering())
print(spill)'''




# Kode for å generere GUI'et

class GUITournament(Frame):
    # Klassen GUITournament definerer en turnering mellom menneske
    # og en Spiller
    spiller = None
    # Resultater holder resultatet av kampene - for plotting
    resultater = None
    # Denne labelen vil brukes for aa rapportere enkeltspill
    resultat_label = None

    def __init__(self, parent, motspiller):
        Frame.__init__(self, parent)
        self.parent = parent
        # Huske hvem vi spiller mot
        self.spiller = motspiller
        # Initiere listen av resultater
        self.resultater = []
        # Foreloepig ikke noe aa rapportere
        self.resultat_label = StringVar()
        self.resultat_label.set("Beskrivelse av siste spill kommer her")
        self.style = Style()
        self.fig = None


    def arranger_enkeltspill(self, action):
        userAction = action
        aiAction = self.spiller.velg_aksjon()
        if isinstance(self.spiller, Historiker) or isinstance(self.spiller, MestVanlig):
            self.spiller.addAction(userAction)
        if userAction.__gt__(aiAction):  # if user wins, add 1 point
            self.resultater.append(1)
        elif userAction.__eq__(aiAction):  # if tie, add 0.5 points to both
            self.resultater.append(0.5)
        else:
            self.resultater.append(0)  # AI wins, add 1 point



    def setup_gui(self):
        self.parent.title("Stein - Saks - Papir")
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)
        # Label for rapportering
        label = Label(self.parent, textvariable=self.resultat_label)
        label.place(x=800, y=50)
        # Buttons
        # Disse fyrer av metoden self.arranger_enkeltspill som er
        # definert i klassen. Denne metoden tar aksjonen til mennesket
        # som startup, og gjennomfoerer spillet
        # Samme type oppfoersel for de tre aksjons-knappene
        rock_button = Button(self, text="Stein",
                             command=lambda: self.arranger_enkeltspill(Aksjon("Stein")))
        rock_button.place(x=800, y=400)
        scissors_button = Button(self, text="Saks",
                                 command=lambda: self.arranger_enkeltspill(Aksjon("Saks")))
        scissors_button.place(x=900, y=400)
        paper_button = Button(self, text="Papir",
                              command=lambda: self.arranger_enkeltspill(Aksjon("Papir")))
        paper_button.place(x=1000, y=400)
        # quit_button avslutter GUI'et naar den trykkes
        quit_button = Button(self, text="Quit", command=self.quit)
        quit_button.place(x=1000, y=450)
        # Embedde en graf i vinduet for aa rapportere fortloepende score
        self.fig = FigureCanvasTkAgg(pylab.figure(), master=self)
        self.fig.get_tk_widget().grid(column=0, row=0)
        self.fig.show()


        plt.figure(self.fig.figure.number)  # Handle til figuren
        plt.ion()
        plt.plot(range(1, len(self.resultater) + 1),
                 100 * numpy.cumsum(self.resultater) / range(1, len(self.resultater) + 1), 'b-', lw=4)
        plt.ylim([0, 100])
        plt.xlim([1, max(1.1, len(self.resultater))])
        plt.plot(plt.xlim(), [50, 50], 'k--', lw=2)
        plt.grid(b=True, which='both', color='0.65', linestyle='-')
        self.fig.show()



# Styrer spiller gjennom Tkinter/GUI.
root = Tk()
# Definer et vindu med gitte dimensjoner
root.geometry("1100x500+300+300")
# Lag instans, og kjoer oppsett av GUI (knapper etc)
GUITournament(root, Historiker(2)).setup_gui()
# Vis vindu, og utfoer tilhoerende kommandoer
root.mainloop()