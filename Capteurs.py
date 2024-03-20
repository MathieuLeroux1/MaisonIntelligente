class Capteurs:
    def __init__(self, lock, mode = "Local"):
        self.lock = lock
        self.mode = mode
    
    def lire_capteurs(self):
        pass
        
    def mettre_a_jour_lcd(self, temperature, humidite):
        pass
        
    def publier_informations(self, temperature, humidite, mode):
        pass

    def set_mode(self, mode):
        self.mode = mode
    