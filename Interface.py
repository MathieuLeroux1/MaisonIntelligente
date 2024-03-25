import grovepi
import time
import Temp
import Wet
import threading

class InterfaceUtilisateur:
    modes = ["Local", "Distant", "Quitter"]
    def __init__(self, lock, bouton_pin):
        with self.lock:
            self.lock = lock
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
        temperature_cible = 0 
        humidite_cible = 0
        mode_selectionne = None
        RotaryPin = 1
        tempe = Temp()
        Wets = Wet()
        grovepi.pinMode(RotaryPin,"INPUT")

        #Waiting Room
        while not self.bouton_appuye():
            pass

        # Modification de la température        
        while not self.bouton_appuye():
            sensor_value = grovepi.analogRead(RotaryPin)
            degree = map(sensor_value,0,1023,0,30)
            tempe.SetTempCible(degree)
            temperature_cible = degree

        # Modification de l'humidité           
        while not self.bouton_appuye():
            sensor_value = grovepi.analogRead(RotaryPin)
            degree = map(sensor_value,0,1023,0,100)
            Wets.SetWetTarget(degree)
            humidite_cible = degree

        # Sélection du mode     
        while not self.bouton_appuye():
            sensor_value = grovepi.analogRead(RotaryPin)
            degree = map(sensor_value,0,1023,0,2)
            mode_selectionne = self.modes[degree]

        return temperature_cible, humidite_cible, mode_selectionne

