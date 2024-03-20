import grovepi

class Temp:

    temp = 0
    tempCible = None
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
    



