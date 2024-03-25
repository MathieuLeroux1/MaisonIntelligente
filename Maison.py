#Philippe Robichaud-Gionet et Mathieu Leroux
import threading
import Capteurs
import Interface
import Actions


class Maison:
    def __init__(self):
        self.lock = threading.Lock()
        self.courtier = "test.mosquitto.org"
        self.port_courtier = 1883
        self.sujet = "clg/kf1/maison/temp"
        self.capteurs = None


    def demarrer(self):
        self.capteurs = Capteurs(self.lock, self.courtier, self.port_courtier, self.sujet)
        pass

maison_intelligente = Maison()
maison_intelligente.demarrer()