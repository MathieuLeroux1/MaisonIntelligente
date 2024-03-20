import grovepi
import time

class Temp:

    temp = 0
    tempCible = None
    
    def __init__(self):
        [temp,humidity] = grovepi.dht(2,0)
        self.temp = temp

    #GET temp
    def GetTemp(self):
        return self.temp
    #SET temp
    def SetTemp(self,newValue):
        self.temp = newValue

    #GET TempCible
    def GetTempCible(self):
        return self.tempCible
    #SET TempCible
    def SetTempCible(self,newValue):
        if (not(newValue < 0 or newValue > 30)):
            self.tempCible = newValue
    

    #Compare Activation Chauffage
    def CompareTemp(self): 
        ValStart = self.tempCible - self.temp == 2
        time.sleep(10)
        ValEnd = self.tempCible - self.temp == 2
        return ValStart == ValEnd



