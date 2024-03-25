import paho.mqtt.client as mqtt
import grovepi
import math
import time

class Capteurs:


    def __init__(self, lock, courtier, port_courtier, sujet, mode="Local"):
        self.lock = lock
        self.mode = mode
        self.courtier = courtier
        self.port_courtier = port_courtier
        self.sujet = sujet

        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "Equipe1")
        self.client.connect(self.courtier, self.port_courtier)

    def lire_capteurs(self):
        with self.lock:
            temperature, humidite = grovepi.dht(7, 0) 
            return temperature, humidite
        
    def mettre_a_jour_lcd(self, temperature, humidite):
        pass
        
    def publier_informations(self, temperature, humidite):
        payload = "Température: {}°C, Humidité: {}%".format(temperature, humidite)
        self.client.publish(self.sujet, payload)

    def set_mode(self, mode):
        self.mode = mode        