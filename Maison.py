#Philippe Robichaud-Gionet et Mathieu Leroux
import threading

class Maison:
    def __init__(self):
        self.lock = threading.Lock()

    def demarrer(self):
        pass


maison_intelligente = Maison()
maison_intelligente.demarrer()