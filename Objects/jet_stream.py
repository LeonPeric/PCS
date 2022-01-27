import math
import numpy as np


class alt_Jet_stream():
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
        self.constant = (self.g * self.c * self.b) * self.height * (1 - (self.height) / (2 * self.ZT)) * (math.cos(self.latitude) ** 2) * (math.sin(self.latitude) ** 2)/1000
        self.speed = 0

    def calc_speed(self, temperature):
        """
        Calculates the current speed of the jet stream

        Attributes:
            temperature: float
                Current temperature in kelvin
        """
        self.speed = self.constant / (self.Omega * temperature)


class Jet_stream():

    def __init__(self, average_thickness, time_diff, dt, scale=1):
        self.min_speed = 80/3.6
        self.max_speed = 160/3.6
        self.average_speed = (self.max_speed - self.min_speed) / 2
        self.average_thickness = average_thickness
        self.time_diff = time_diff
        self.in_stream = False
        self.time_since_last = 0
        self.distance_start = 0
        self.stream_thickness = 0
        self.speed = 0
        self.dt = dt
        self.scale = scale
        self.time_till_next = np.random.normal(self.time_diff, self.scale * 10, size = None)
        

    def check_jet_stream(self, current_distance):
        if not self.in_stream:
            self.in_stream = self.time_since_last >= self.time_till_next
            if self.in_stream:
                self.distance_start = current_distance
                self.stream_thickness = np.random.normal(self.average_thickness, scale=self.scale * 1000, size=None)
                self.speed = np.random.normal(self.average_speed, scale=20 - 20 / (1 + self.scale) , size = None)
            else:
                self.time_since_last += self.dt
        else:
            self.in_stream = not (current_distance - self.distance_start >= self.stream_thickness)
            if not self.in_stream:
                self.time_since_last = 0
                self.time_till_next = np.random.normal(self.time_diff, scale=self.scale * 60, size = None)