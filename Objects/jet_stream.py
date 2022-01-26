import math

class Jet_stream():
    """
    Calculates the speed of the jet stream

    Attributes:
        latitude: float
            latitude of where the plane is flying
        height: float
            altitude of the plane in m
    
    Methods:
        calc_speed(temperature):
            calculates the current speed of the jet stream
    """
    def __init__(self, latitude, height) -> None:
        self.Omega = 1.456 * (10 ** (-4))
        self.g = 9.81
        self.ZT = 17000
        self.c = 1.18 * (10 ** (-3))
        self.b = 40
        self.latitude = latitude
        self.height = height 
        self.constant = (self.g * self.c * self.b) * self.height * (1 - (self.height) /( 2 * self.ZT)) * (math.cos(self.latitude) ** 2) * (math.sin(self.latitude) ** 2)/1000
        self.speed = 0

    def calc_speed(self, temperature):
        """
        Calculates the current speed of the jet stream

        Attributes:
            temperature: float
                Current temperature in kelvin
        """
        self.speed =  self.constant / (self.Omega * temperature) 
