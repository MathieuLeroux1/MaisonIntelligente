from temp import Temp
from Wet import Wet
import threading
import grovepi
import time

class Actions:

    tempDelRed = 3
    WetDelBlue = 4
    MoveDelGreen = 6
    MoveDetector = 7
    LightDetector = 0
    ThreadAct = ""
    CheckTemp = ""
    CheckWet = ""

    def __init__(self, lock):
        self.lock = lock
        self.CheckTemp = Temp()
        self.CheckWet = Wet()
        self.ThreadAct = threading.Thread(target=self.threadAction) 
        self.ThreadAct.start()
        
    def activer_chauffage(self):
       grovepi.digitalWrite(self.tempDelRed,1)
        
    def desactiver_chauffage(self):
        grovepi.digitalWrite(self.tempDelRed,0)
        pass
        
    def activer_deshumidificateur(self):
        grovepi.digitalWrite(self.WetDelBlue,1)
        pass
        
    def desactiver_deshumidificateur(self):
        grovepi.digitalWrite(self.WetDelBlue,0)
        pass

    def CheckMovingPlusLight(self):
        grovepi.pinMode(self.MoveDetector, "INPUT")
        grovepi.pinMode(self.LightDetector, "INPUT")

        if (grovepi.digitalRead(self.MoveDetector) and grovepi.analogRead(self.LightDetector)):
            grovepi.digitalWrite(self.MoveDelGreen,1)
            time.sleep(10)
            grovepi.digitalWrite(self.MoveDelGreen,0)

    def threadAction(self):
        if (self.CheckTemp.CompareTemp()):
            self.activer_chauffage()
        else:
            self.desactiver_chauffage()

        if (self.CheckWet.CompareHumidtity()):
            self.activer_deshumidificateur()
        else:
            self.desactiver_deshumidificateur()

        self.CheckMovingPlusLight()

