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
<<<<<<< HEAD
 
=======
        mode_selectionne = None
        RotaryPin = 1
        tempe = Temp()
        Wets = Wet()
        grovepi.pinMode(RotaryPin,"INPUT")

        #Waiting Room
        while not self.bouton_appuye():
            pass
        
>>>>>>> bf5dcec986148d492a3b257e26d85850c77a6a78
        # Modification de la température cible
        while not self.bouton_appuye():
            with self.lock:
                sensor_value = grovepi.analogRead(self.RotaryPin)
                degree = map(sensor_value,0,1023,0,30)
<<<<<<< HEAD
                self.tempe.SetTempCible(degree)
                self.capteurs.mettre_a_jour_lcd("Température cible: {}°C".format(self.tempe.GetTempCible()))
=======
                tempe.SetTempCible(degree)
                self.capteurs.mettre_a_jour_lcd("Température cible: {}°C".format(tempe.GetTempCible()))
>>>>>>> bf5dcec986148d492a3b257e26d85850c77a6a78

        # Modification de l'humidité cible
        while not self.bouton_appuye():
            with self.lock:
                sensor_value = grovepi.analogRead(self.RotaryPin)
                degree = map(sensor_value,0,1023,0,100)
<<<<<<< HEAD
                self.Wets.SetWetTarget(degree)
                self.capteurs.mettre_a_jour_lcd("Humidité cible: {}°C".format(self.Wets.GetWetTarget()))
=======
                Wets.SetWetTarget(degree)
                self.capteurs.mettre_a_jour_lcd("Humidité cible: {}°C".format(Wets.GetWetTarget()))
>>>>>>> bf5dcec986148d492a3b257e26d85850c77a6a78

        # Sélection du mode
        while not self.bouton_appuye():
           with self.lock:
            sensor_value = grovepi.analogRead(self.RotaryPin)
            mode_selectionne = map(sensor_value,0,1023,0,2)
            self.capteurs.mettre_a_jour_lcd("Mode: {}°C".format(mode_selectionne))
            self.capteurs.set_mode(mode_selectionne)
    
