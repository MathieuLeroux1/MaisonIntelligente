import grovepi
import time
from temp import Temp
from Wet import Wet
import threading

class Interface:
    modes = ["Local", "Distant", "Quitter"]
    def __init__(self, lock, bouton_pin):
        self.lock = lock
        with self.lock:
            self.bouton_pin = bouton_pin
            #Input mode des device
            RotaryPin = 1
            grovepi.pinMode(RotaryPin,"INPUT")
            grovepi.pinMode(self.bouton_pin, "INPUT")
            #Instance des objets Temp et Wet
            self.tempe = Temp()
            self.Wets = Wet()
            #Mesure des valeurs température et humidité
            [temp,humid] = grovepi.dht(2,0)
            self.tempe.SetTemp(temp)
            self.Wets.SetWet(humid)
            #Création du thread et exécution du thread Interface
            self.thread = threading.Thread(target=self.changer_interface())
            self.thread.start()

          
    def bouton_appuye(self):
        with self.lock:
            while True:
                etat_bouton = grovepi.digitalRead(self.bouton_pin)
                if etat_bouton == 1:
                    return True
                time.sleep(0.1)

    def changer_interface(self):

        while not self.bouton_appuye():  
        # Modification de la température cible
            with self.lock:
                sensor_value = grovepi.analogRead(self.RotaryPin)
                degree = map(sensor_value,0,1023,0,30)
                self.tempe.SetTempCible(degree)
                

        while not self.bouton_appuye():
        # Modification de l'humidité cible
            with self.lock:
                sensor_value = grovepi.analogRead(RotaryPin)
                degree = map(sensor_value,0,1023,0,100)
                Wets.SetWetTarget(degree)
                humidite_cible = degree
                 
        while not self.bouton_appuye():
        # Sélection du mode
            with self.lock:
                sensor_value = grovepi.analogRead(RotaryPin)
                degree = map(sensor_value,0,1023,0,2)
                mode_selectionne = self.modes[degree]
