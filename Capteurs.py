import paho.mqtt.client as mqtt
import grovepi
from temp import Temp
from Wet import Wet
from Interface import Interface
from grove_rgb_lcd import *
from time import sleep

class Capteurs:
    def __init__(self, lock, courtier, port_courtier, sujet, mode="Local"):
        self.lock = lock
        self.mode = mode
        self.temp_obj = Temp()
        self.wet_obj = Wet()
        self.courtier = courtier
        self.port_courtier = port_courtier
        self.sujet = sujet
        self.temperature_equipier = None

        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "Equipe1")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.courtier, self.port_courtier)

    def on_connect(self, client, userdata, flags, rc):
        client.subscribe(self.sujet)
    
    def on_message(self,client,userdata,message):
        with self.lock:
            self.temperature_equipier = message.payload.decode()
            Temp.setText("Distant: Température: °C")

    def lire_capteurs(self):
        with self.lock:
            temperature = self.temp_obj.GetTemp()
            humidite = self.wet_obj.GetWet()
            return temperature, humidite

    def lireValeursDistantes(self, client):
        client.loop_start()
        while(True):
            with self.lock:
                if(self.temperature_equipier == None):
                    sleep(1)
                else:
                    break
        client.loop_stop()
        
        
    def mettre_a_jour_lcd(self, temperature, humidite):
        with self.lock:
            if self.mode == "Local":
                texte = "Local: Température: {}°C, Humidité: {}%".format(temperature, humidite)
                Temp.setText(texte)
            elif self.mode == "Distant":
                self.lireValeursDistantes(self.client)
            else:
                self.client.disconnect

    def publier_informations(self, temperature, humidite):
        payload = "Local: Température: {}°C, Humidité: {}%".format(temperature, humidite)
        self.client.publish(self.sujet, payload)

    def set_mode(self, mode):
        self.mode = mode
  