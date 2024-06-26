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
            self.thread = threading.Thread(target=self.BtnPress())
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
        while grovepi.digitalRead(self.bouton_pin) == 0:
            time.sleep(0.5)
            while grovepi.digitalRead(self.bouton_pin) == 1:
                time.sleep(0.5)
                while grovepi.digitalRead(self.bouton_pin) == 0:
                    return True
        return False
    
    
    def BtnPress(self):
        while True:
            while not grovepi.digitalRead(self.bouton_pin):
                #get value rotary and translate to 0 - 30
                sensor_value = grovepi.analogRead(self.RotaryPin)
                voltage = round((float)(sensor_value) * 5 / 1023, 2)
                degrees = round((voltage * 300) / 5, 2)
                degree = int(degrees / 300 * 30)
                #Set temperature cible et print LCD
                self.tempe.SetTempCible(degree)
                self.capteurs.mettre_a_jour_lcd("Temperature cible: {} Celcius".format(self.tempe.GetTempCible()))
            time.sleep(0.5)
            while not grovepi.digitalRead(self.bouton_pin):
                #get value rotary and translate to 0 - 100
                sensor_value = grovepi.analogRead(self.RotaryPin)
                voltage = round((float)(sensor_value) * 5 / 1023, 2)
                degrees = round((voltage * 300) / 5, 2)
                degree = int(degrees / 300 * 100)
                #Set Humidity cible et print LCD
                self.Wets.SetWetTarget(degree)
                self.capteurs.mettre_a_jour_lcd("Humidite cible: {}%".format(self.Wets.GetWetTarget()))
            time.sleep(0.5)
            while not grovepi.digitalRead(self.bouton_pin):
                sensor_value = grovepi.analogRead(self.RotaryPin)
                voltage = round((float)(sensor_value) * 5 / 1023, 2)
                degrees = round((voltage * 300) / 5, 2)
                mode_selectionne = int(degrees / 300 * 2)
                self.capteurs.mettre_a_jour_lcd("Mode: {}°C".format(mode_selectionne))
                self.capteurs.set_mode(mode_selectionne)
            time.sleep(0.5)


    def changer_interface(self):
        try:
            self.BtnPress("ModifTemp")
            self.BtnPress("ModifHumid")                
            self.BtnPress("SelectMode")              
        except Exception as e:
            print("An exception occurred:", e)
    """         
    def changer_interface(self):
        self.est_clique()

        self.BtnPress("ModifTemp")

        self.est_clique()

        self.BtnPress("ModifHumid")

        self.est_clique()

        self.BtnPress("SelectMode")

        self.est_clique()

        self.bouton_appuye()
        

        # Attendre l'appui sur le bouton
        #while not self.est_clique():
            #pass
                
        # Modification de la température cible
        while not self.BtnPress("ModifTemp"):
            print("Zone Temp")
                #sensor_value = grovepi.analogRead(self.RotaryPin)
                #degree = map(sensor_value, 0, 1023, 0, 30)
                #self.tempe.SetTempCible(degree)
                #self.capteurs.mettre_a_jour_lcd("Température cible: {}°C".format(self.tempe.GetTempCible()))

        # Modification de l'humidité cible
        while not self.BtnPress("ModifHumid"):
                        print("Zone Humidity")
                #sensor_value = grovepi.analogRead(self.RotaryPin)
                #degree = map(sensor_value, 0, 1023, 0, 100)
                #self.Wets.SetWetTarget(degree)
                #self.capteurs.mettre_a_jour_lcd("Humidité cible: {}°C".format(self.Wets.GetWetTarget()))
                #print("Je suis dans zone temp")                

        # Sélection du mode
        while not self.BtnPress("SelectMode"):
                        print("Zone Mode")
                #sensor_value = grovepi.analogRead(self.RotaryPin)
                #mode_selectionne = map(sensor_value, 0, 1023, 0, 2)
                #self.capteurs.mettre_a_jour_lcd("Mode: {}°C".format(mode_selectionne))
                #self.capteurs.set_mode(mode_selectionne)
                #print("Je suis dans zone temp")                

        # Attendre l'appui sur le bouton pour terminer
        while not self.bouton_appuye():
            pass

    """ 
