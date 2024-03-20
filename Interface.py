import grovepi
import time
import threading

class InterfaceUtilisateur:
    mode = ["Local", "Distant", "Quitter"]

    def __init__(self, lock, bouton_pin):
        with self.lock:
            self.lock = lock
            self.bouton_pin = bouton_pin
            grovepi.pinMode(self.bouton_pin, "INPUT")
          
    def bouton_appuye(self):
        with self.lock:
            while True:
                etat_bouton = grovepi.digitalRead(self.bouton_pin)
                if etat_bouton == 1:
                    return True
                time.sleep(0.1)

    def changer_interface(self):
        temperature_cible = None
        humidite_cible = None
        mode_selectionne = None

        while not self.bouton_appuye():
            pass

        # Modification de la température
        
        while not self.bouton_appuye():
            pass

        # Modification de l'humidité
        
        while not self.bouton_appuye():
            pass

        # Sélection du mode
        
        while not self.bouton_appuye():
            pass

        return temperature_cible, humidite_cible, mode_selectionne

