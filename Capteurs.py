import paho.mqtt.client as mqtt
import grovepi
from temp import Temp
from Wet import Wet
from grove_rgb_lcd import *
from time import sleep
import threading

class Capteurs:
    lock = ""
    temp_initale = ""
    wet_initiale = ""
    mode = ""
    courtier = ""
    port_courtier = ""
    sujet = ""
    temperature_equipier = ""
    thread = ""

    def __init__(self, lock, courtier, port_courtier, sujet, mode="Local"):
        self.lock = lock
        self.temp_initale = Temp()
        self.wet_initiale = Wet()
        
        #self.mettre_a_jour_lcd("Température: " + str(self.temp_initale.GetTemp()) + "; Humidité: " + str(self.wet_initiale.GetWet()))
        
        self.mode = mode
        self.courtier = courtier
        self.port_courtier = port_courtier
        self.sujet = sujet
        self.temperature_equipier = None
        self.thread = threading.Thread(target=self.publier_informations())
        try:
            self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "Equipe1")
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            self.client.connect(self.courtier, self.port_courtier)
        except:
            print()

    def on_connect(self, client, userdata, flags, rc):
        client.subscribe(self.sujet)
    
    def on_message(self,client,userdata,message):
        with self.lock:
            self.temperature_equipier = message.payload.decode()
            Temp.setText(self.temperature_equipier)

    def lireValeursDistantes(self, client):
        client.loop_start()
        while(True):
            with self.lock:
                if(self.temperature_equipier == None):
                    sleep(1)
                else:
                    break
        client.loop_stop()
         
    def mettre_a_jour_lcd(self, texte):
        if self.mode == "Local":
            setText_norefresh(texte) # type: ignore
        elif self.mode == "Distant":
            self.lireValeursDistantes(self.client)
        else:
            self.client.disconnect()

    def publier_informations(self, temperature, humidite):
        payload = "Local: Température: {}°C, Humidité: {}%, Température cible: {}°C, Humidité cible: {}%".format(temperature, humidite, Temp.GetTempCible(), Wet.GetWetTarget())
        self.client.publish(self.sujet, payload)

    def set_mode(self, mode):
        self.mode = mode
  