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

    def demarrer(self):
        pass

maison_intelligente = Maison()
maison_intelligente.demarrer()