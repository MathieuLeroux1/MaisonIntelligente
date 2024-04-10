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
            self.RotaryPin = 1
            grovepi.pinMode(self.RotaryPin,"INPUT")
            grovepi.pinMode(self.bouton_pin, "INPUT")
            #Instance des objets Temp et Wet
            self.tempe = self.capteurs.temp_initale
            self.Wets = self.capteurs.wet_initiale
            #Création du thread et exécution du thread Interface
            self.thread = threading.Thread(target=self.changer_interface())
            self.thread.start()
         
    def bouton_appuye(self):
        bouton_presse = False
        while not bouton_presse:
            etat_bouton = grovepi.digitalRead(self.bouton_pin)
            if etat_bouton == 1:
                bouton_presse = True
            time.sleep(0.5)
        return True

    def est_clique(self):
        if grovepi.digitalRead(self.port_btn) == 0:
            time.sleep(0.5)
            if grovepi.digitalRead(self.port_btn) == 1:
                time.sleep(0.5)
                if grovepi.digitalRead(self.port_btn) == 0:
                    return True
        return False
    
    
    def BtnPress(self,zone):
        BtnPress = False
        while not BtnPress:
            if (grovepi.digitalRead(self.bouton_pin)):
                BtnPress = True
            time.sleep(0.5)

            if (zone == "ModifTemp"):
                print("salut")
                sensor_value = grovepi.analogRead(self.RotaryPin)
                degree = map(sensor_value, 0, 1023, 0, 30)
                self.tempe.SetTempCible(degree)
                try:
                    self.capteurs.mettre_a_jour_lcd("Température cible: {}°C".format(self.tempe.GetTempCible()))
                except Exception as e:
                    print("bug LCD")
            elif (zone == "ModifHumid"):
                sensor_value = grovepi.analogRead(self.RotaryPin)
                degree = map(sensor_value, 0, 1023, 0, 100)
                self.Wets.SetWetTarget(degree)
                self.capteurs.mettre_a_jour_lcd("Humidité cible: {}°C".format(self.Wets.GetWetTarget()))
            elif (zone == "SelectMode"):
                sensor_value = grovepi.analogRead(self.RotaryPin)
                mode_selectionne = map(sensor_value, 0, 1023, 0, 2)
                self.capteurs.mettre_a_jour_lcd("Mode: {}°C".format(mode_selectionne))
                self.capteurs.set_mode(mode_selectionne)



    def changer_interface(self):
        # Attendre l'appui sur le bouton
        while not self.est_clique():
            pass
        
        print("Boutton Cliqué.")
        
        # Modification de la température cible
        while not self.BtnPress("ModifTemp"):
            pass
                #sensor_value = grovepi.analogRead(self.RotaryPin)
                #degree = map(sensor_value, 0, 1023, 0, 30)
                #self.tempe.SetTempCible(degree)
                #self.capteurs.mettre_a_jour_lcd("Température cible: {}°C".format(self.tempe.GetTempCible()))

        # Modification de l'humidité cible
        while not self.BtnPress("ModifHumid"):
            pass
                #sensor_value = grovepi.analogRead(self.RotaryPin)
                #degree = map(sensor_value, 0, 1023, 0, 100)
                #self.Wets.SetWetTarget(degree)
                #self.capteurs.mettre_a_jour_lcd("Humidité cible: {}°C".format(self.Wets.GetWetTarget()))
                #print("Je suis dans zone temp")                

        # Sélection du mode
        while not self.BtnPress("SelectMode"):
            pass
                #sensor_value = grovepi.analogRead(self.RotaryPin)
                #mode_selectionne = map(sensor_value, 0, 1023, 0, 2)
                #self.capteurs.mettre_a_jour_lcd("Mode: {}°C".format(mode_selectionne))
                #self.capteurs.set_mode(mode_selectionne)
                #print("Je suis dans zone temp")                

        # Attendre l'appui sur le bouton pour terminer
        while not self.bouton_appuye():
            pass
