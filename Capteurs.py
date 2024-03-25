import paho.mqtt.client as mqtt
import grovepi
import Temp
import Wet

class Capteurs:
    def __init__(self, lock, courtier, port_courtier, sujet, mode="Local"):
        self.lock = lock
        self.mode = mode
        self.temp_obj = Temp.Temp()
        self.wet_obj = Wet.Wet()
        self.courtier = courtier
        self.port_courtier = port_courtier
        self.sujet = sujet

        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "Equipe1")
        self.client.on_connect = self.on_connect
        self.client.connect(self.courtier, self.port_courtier)

    def on_connect(self, client, userdata, flags, rc):
        client.subscribe(self.sujet)
    
    def lire_capteurs(self):
        with self.lock:
            temperature = self.temp_obj.GetTemp()
            humidite = self.wet_obj.GetWet()
            return temperature, humidite

        
    def mettre_a_jour_lcd(self, temperature, humidite):
        if(self.mode == "Local"):
            pass
        elif(self.mode == "Distant"):
            pass
        else:
            self.client.disconnect
        
    def publier_informations(self, temperature, humidite):
        if self.mode == "Local":
            payload = "Local: Température: {}°C, Humidité: {}%".format(temperature, humidite)
        elif self.mode == "Distant":
            payload = "Distant: Température: {}°C, Humidité: {}%".format(temperature, humidite)
        self.client.publish(self.sujet, payload)

    def set_mode(self, mode):
        self.mode = mode
  