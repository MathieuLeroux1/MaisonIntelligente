#Philippe Robichaud-Gionet et Mathieu Leroux
import threading
from Capteurs import Capteurs
from Interface import Interface
from Actions import Actions
#LCD Screen:I2C-2 || Boutton:D5 || Green LED:D6 || Red LED:D3 || Blue LED:D4 || Temperature and Humidity:D2 || 
#Rotary Angle:A1 || Light Detector:A0 || Move Detector:D7  

class Maison:
    def __init__(self):
        self.lock = threading.Lock()
        self.courtier = "test.mosquitto.org"
        self.port_courtier = 1883
        self.sujet = "clg/kf1/maison/temp"
        self.capteurs = None
        self.Actions = None
        self.Interface = None

    def demarrer(self):
        self.capteurs = Capteurs(self.lock, self.courtier, self.port_courtier, self.sujet)
        self.Actions = Actions(self.lock)
        self.Interface = Interface(self.lock,"5", self.capteurs)
        pass

maison_intelligente = Maison()
maison_intelligente.demarrer()