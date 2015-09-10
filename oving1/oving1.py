import random
import matplotlib.pyplot as plt
from tkinter import Tk, BOTH, StringVar
from tkinter.ttk import Frame, Button, Label, Style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from numpy import cumsum

__author__ = 'Vemund'


class Action:

    actions = ["rock", "paper", "scissor"]

    def __init__(self, action_number):
        self.action = Action.actions[action_number]

    def __eq__(self, other):
        return self.action == other.action

    def __gt__(self, other):
        if self.action == "rock" and other.action == "scissor":
            return True
        elif self.action == "scissor" and other.action == "paper":
            return True
        elif self.action == "paper" and other.action == "rock":
            return True
        else:
            return False

    def __str__(self):
        return self.action


class Player:

    def __init__(self, mode):
        self.mode = mode
        self.navn = "default player"

        #Counter for sequence CPU
        self.sequence_counter = random.randint(0, 2)

        #Counters for history CPU
        self.other_action_counter = {"rock": 0, "paper": 0, "scissor": 0}

        #List of results from games. The length of the list is the same as number_of_games
        self.results = []

        self.enemy_actions = []

    def velg_aksjon(self):
        if self.mode == "random":
            return self.velg_random()
        elif self.mode == "sequence":
            return self.velg_sequence()
        elif self.mode == "frequency":
            return self.velg_frekvens()
        elif self.mode[0:7] == "history":
            return self.velg_history()
        else:
            return Action(random.randint(0, 2))

    def velg_history(self):
        self.history_counter = {"rock": 0, "paper": 0, "scissor": 0}
        self.history_level = int(self.mode[7:])
        if len(self.enemy_actions) <= self.history_level:
            return self.velg_random()
        for i in range(0,len(self.enemy_actions)-self.history_level):
            if self.enemy_actions[i:i+self.history_level] == self.enemy_actions[-self.history_level:]:
                self.history_counter[self.enemy_actions[i+self.history_level]] += 1

        predicted_move = "rock"
        predicted_move_counter = self.history_counter["rock"]
        for key in self.history_counter:
            if self.history_counter[key] > predicted_move_counter:
                predicted_move = key
                predicted_move_counter = self.history_counter[key]
        return Action((Action.actions.index(predicted_move)+1) % 3)

    def velg_frekvens(self):
        if len(self.results) == 0:
            return self.velg_random() #Velg random i forste trekk
        else:
            if self.other_action_counter["rock"] == self.other_action_counter["paper"] and \
                            self.other_action_counter["paper"] == self.other_action_counter["scissor"]:
                return self.velg_random()
            else:
                most_used_move = "rock"
                most_used_move_counter = self.other_action_counter["rock"]
                for key in self.other_action_counter:
                    if self.other_action_counter[key] > most_used_move_counter:
                        most_used_move = key
                        most_used_move_counter = self.other_action_counter[key]
                return Action((Action.actions.index(most_used_move)+1) % 3)

    def velg_random(self):
        return Action(random.randint(0, 2))

    def velg_sequence(self):
        self.sequence_counter += 1
        return Action(self.sequence_counter % 3)

    def motta_resultat(self, theirAction, score):
        self.other_action_counter[theirAction.__str__()] += 1
        self.enemy_actions.append(theirAction.__str__())
        self.results.append(score)

    def set_name(self, name):
        self.navn = name

    def get_number_of_wins(self):
        a = 0
        for i in self.results:
            if i == 1:
                a += 1
        return a

    def __str__(self):
        return self.navn


class Game:

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.winner = -1

    def gjennomfoer_spill(self):
        p1action = self.player1.velg_aksjon()
        p2action = self.player2.velg_aksjon()
        if p1action == p2action:
            self.player1.motta_resultat(p2action, 0.5)
            self.player2.motta_resultat(p1action, 0.5)
            self.winner = None
            return p1action,p2action,None
        elif p1action > p2action:
            self.player1.motta_resultat(p2action, 1)
            self.player2.motta_resultat(p1action, 0)
            self.winner = self.player1
            return p1action, p2action, player1
        else:
            self.player1.motta_resultat(p2action, 0)
            self.player2.motta_resultat(p1action, 1)
            self.winner = self.player2
            return p1action, p2action, player2

    def __str__(self, result):
        if self.winner == None:
            return "Spillet endte uavgjort"
        elif self.winner == -1:
            return "Spiller er ikke gjennomfoert"
        else:
            return "Dette spillet er avgjort. Vinneren ble " + self.winner.__str__()


class ManyGames:

    def __init__(self, player1, player2, antall_spill):
        self.player1 = player1
        self.player2 = player2
        self.antall_spill = antall_spill

    def arranger_enkeltspill(self):
        game = Game(self.player1, self.player2)
        p1action, p2action, winner = game.gjennomfoer_spill()
        print(player1.__str__()+":",p1action.__str__()+".",player2.__str__()+":",p2action.__str__()+".","Winner:",winner.__str__())

    def arranger_turnering(self):
        for i in range(self.antall_spill):
            self.arranger_enkeltspill()
        print("Turneringen er ferdig!",self.player1.__str__(),"vant",self.player1.get_number_of_wins(),"ganger.",self.player2.__str__(),"vant",self.player2.get_number_of_wins(),"ganger")
        print(self.player1.__str__()+" vant "+str(((self.player1.get_number_of_wins()/float(self.antall_spill))*100))+"% av gangene.")
        print(self.player2.__str__()+" vant "+str(((self.player2.get_number_of_wins()/float(self.antall_spill)*100)))+"% av gangene.")


class GUITournament(Frame):
    # Klassen GUITournament definerer en turnering mellom menneske og en Spiller

    def __init__(self, parent, motspiller):
        Frame.__init__(self, parent)
        self.parent = parent

        # Dette er motspilleren (CPU)
        self.spiller = motspiller

        # Initiere listen av resultater
        self.resultater = []

        # Foreloepig ikke noe aa rapportere
        self.resultat_label = StringVar()
        self.resultat_label.set("Velkommen til Stein-Saks-Papir!")
        self.style = Style()
        self.fig = None

    def arranger_enkeltspill(self, action):
        #P1 is human
        self.p1action = action
        #P2 is the computer
        self.p2action = self.spiller.velg_aksjon()

        if self.p2action > self.p1action:
            self.resultater.append(1)
            self.spiller.motta_resultat(self.p1action, 1)

            self.resultat_label.set(self.spiller.__str__()+" chose "+self.p2action.__str__()+". You chose "+self.p1action.__str__()+". I won!")
        elif self.p2action == self.p1action:
            self.resultater.append(0.5)
            self.resultat_label.set(self.spiller.__str__()+" chose "+self.p2action.__str__()+". You chose "+self.p1action.__str__()+". I'ts a draw!")
            self.spiller.motta_resultat(self.p1action, 0.5)
        else:
            self.resultater.append(0)
            self.resultat_label.set(self.spiller.__str__()+" chose "+self.p2action.__str__()+". You chose "+self.p1action.__str__()+". You won!")
            self.spiller.motta_resultat(self.p1action, 0)

        # Update plot
        plt.figure(self.fig.figure.number) # Handle til figuren
        plt.plot(range(1, len(self.resultater) + 1),
                 100 * cumsum(self.resultater) /
                 range(1, len(self.resultater) + 1), "b-", lw=4)

        plt.ylim([0, 100]) #Setter y-aksen fra 0-100
        plt.xlim([1,max(1.1, len(self.resultater))]) #Setter x-aksen fra 1 til minst 1.

        plt.plot(plt.xlim(), [50, 50], "k--", lw=1) #Lager en svart strek midt i plottet. Trengs dette aa gjoeres flere ganger?

        plt.grid(b=True, which="both", color="0.65", linestyle="-")
        self.fig.show()

    def setup_gui(self):
        self.parent.title("Stein - Saks - Papir")
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)

        # Label for rapportering
        label = Label(self.parent, textvariable=self.resultat_label)
        label.place(x=750, y=50)

        # Buttons
        # Disse fyrer av metoden self.arranger_enkeltspill som er
        # definert i klassen. Denne metoden tar aksjonen til mennesket
        # som startup, og gjennomfoerer spillet
        # Samme type oppfoersel for de tre aksjons-knappene
        rock_button = Button(self, text="Stein", command=lambda: self.arranger_enkeltspill(Action(0)))
        rock_button.place(x=800, y=400)
        scissors_button = Button(self, text="Saks", command=lambda: self.arranger_enkeltspill(Action(2)))
        scissors_button.place(x=900, y=400)
        paper_button = Button(self, text="Papir", command=lambda: self.arranger_enkeltspill(Action(1)))
        paper_button.place(x=1000, y=400)


        #quit button avslutter GUIet naar den trykkes
        quit_button = Button(self, text="Quit", command=self.quit)
        quit_button.place(x=1000, y=450)

        # Embedde en graf i vinduet for aa rapportere fortloepende score
        self.fig = FigureCanvasTkAgg(plt.figure(), master=self)
        self.fig.get_tk_widget().grid(column=0, row=0)
        self.fig.show()

if __name__ == "__main__":
    player1 = Player("history1")
    player2 = Player("sequence")
    player3 = Player("random")
    player4 = Player("frequency")
    player1.set_name("Historiespiller")
    player2.set_name("Sekvensspiller")
    player3.set_name("Randomspiller")
    player4.set_name("Frekvensspiller")

    # Styrer spiller gjennom Tkinter/GUI.
    root = Tk()

    # Definer et vindu med gitte dimensjoner
    root.geometry("1100x500+300+300")

    # Lag instans, og kjoer oppsett av GUI (knapper etc)
    GUITournament(root, player2).setup_gui()

    # Vis vindu, og utfoer tilhoerende kommandoer
    root.mainloop()

    #games = ManyGames(player1,player2,1000)
    #games.arranger_turnering()
