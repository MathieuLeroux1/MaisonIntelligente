import grovepi
import time

class Wet:
    wet = 0
    wetTarget = None

    def __init__(self):
        [temp,humid] = grovepi.dht(2,0)
        self.wet = humid
    #GET Wet
    def GetWet(self):
        return self.wet + "%"
    #SET Wet
    def SetWet(self,newValue):
        self.wet = newValue
   
    #GET WetTarget
    def GetWetTarget(self):
        return self.wetTarget
    #SET WetTarget
    def SetWetTarget(self,NewValue):
        if (not(NewValue < 0 or NewValue > 100)):
            self.wetTarget = NewValue

    #Compare Humidificator desactivation
    def CompareHumidtity(self):
        self.wetTarget - self.wet == 5
        ValStart = self.wetTarget - self.wet == 5
        time.sleep(10)
        ValEnd = self.wetTarget - self.wet == 5
        return ValStart == ValEnd