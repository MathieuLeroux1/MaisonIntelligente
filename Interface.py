import grovepi
import time
from temp import Temp
from Wet import Wet
import threading
from Capteurs import Capteurs

class Interface:
    modes = ["Local", "Distant", "Quitter"]

    def __init__(self, lock, bouton_pin, capteurs):
        self.lock = lock
        self.capteurs = capteurs
        with self.lock:
            self.bouton_pin = bouton_pin
            #Input mode des device
            RotaryPin = 1
            grovepi.pinMode(RotaryPin,"INPUT")
            grovepi.pinMode(self.bouton_pin, "INPUT")
            #Instance des objets Temp et Wet
            self.tempe = self.capteurs.temp_initale
            self.Wets = self.capteurs.wet_initiale
            #Création du thread et exécution du thread Interface
            self.thread = threading.Thread(target=self.changer_interface())
            self.thread.start()
         
    def bouton_appuye(self):

        while True:
            etat_bouton = grovepi.digitalRead(self.bouton_pin)
            if etat_bouton == 1:
                return True
            time.sleep(0.1)

    def changer_interface(self):
        print(not(self.bouton_appuye()))
        # Attendre l'appui sur le bouton
        while not self.bouton_appuye():
            print("Je suis dans zone attend")
            pass

        # Modification de la température cible
        with self.lock:
            while not self.bouton_appuye():
                sensor_value = grovepi.analogRead(self.RotaryPin)
                degree = map(sensor_value, 0, 1023, 0, 30)
                self.tempe.SetTempCible(degree)
                self.capteurs.mettre_a_jour_lcd("Température cible: {}°C".format(self.tempe.GetTempCible()))
                print("Je suis dans zone temp")

        # Modification de l'humidité cible
        with self.lock:
            while not self.bouton_appuye():
                sensor_value = grovepi.analogRead(self.RotaryPin)
                degree = map(sensor_value, 0, 1023, 0, 100)
                self.Wets.SetWetTarget(degree)
                self.capteurs.mettre_a_jour_lcd("Humidité cible: {}°C".format(self.Wets.GetWetTarget()))
                print("Je suis dans zone temp")                

        # Sélection du mode
        with self.lock:
            while not self.bouton_appuye():
                sensor_value = grovepi.analogRead(self.RotaryPin)
                mode_selectionne = map(sensor_value, 0, 1023, 0, 2)
                self.capteurs.mettre_a_jour_lcd("Mode: {}°C".format(mode_selectionne))
                self.capteurs.set_mode(mode_selectionne)
                print("Je suis dans zone temp")                

        # Attendre l'appui sur le bouton pour terminer
        while not self.bouton_appuye():
            pass
