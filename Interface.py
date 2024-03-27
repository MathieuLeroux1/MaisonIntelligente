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
            grovepi.pinMode(self.bouton_pin, "INPUT")
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
        mode_selectionne = None
        RotaryPin = 1
        tempe = Temp()
        Wets = Wet()
        grovepi.pinMode(RotaryPin,"INPUT")

        #Waiting Room
        while not self.bouton_appuye():
            pass
        
        # Modification de la température cible
        while not self.bouton_appuye():
            with self.lock:
                sensor_value = grovepi.analogRead(RotaryPin)
                degree = map(sensor_value,0,1023,0,30)
                tempe.SetTempCible(degree)
                self.capteurs.mettre_a_jour_lcd("Température cible: {}°C".format(tempe.GetTempCible()))

        # Modification de l'humidité cible
        while not self.bouton_appuye():
            with self.lock:
                sensor_value = grovepi.analogRead(RotaryPin)
                degree = map(sensor_value,0,1023,0,100)
                Wets.SetWetTarget(degree)
                self.capteurs.mettre_a_jour_lcd("Humidité cible: {}°C".format(Wets.GetWetTarget()))

        # Sélection du mode
        while not self.bouton_appuye():
           with self.lock:
            sensor_value = grovepi.analogRead(RotaryPin)
            degree = map(sensor_value,0,1023,0,2)
            mode_selectionne = self.modes[degree]
            self.capteurs.mettre_a_jour_lcd("Mode: {}°C".format(mode_selectionne))
            self.capteurs.set_mode(mode_selectionne)
    
        while not self.bouton_appuye():
            pass