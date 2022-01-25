import random
import numpy as np

class Temperature():
    """
    Object for all temperature related operations in the simulation
    Attributes:
        scale: int
            The amount of variation from the average temperature
        change: float
            How much the temperature can change per time step
        avg_temp: float
            The average temperature for the simulation in kelvin
        dt: float
            Timestep in second

    Methods:
        changetemp():
            Changes the current temperature.
    """
    def __init__(self, scale, change, avg_temp, dt) -> None:
        self.temp = np.random.normal(avg_temp,scale, size=None)
        self.mintemp = avg_temp - 3 * scale
        self.maxtemp = avg_temp + 3 * scale
        self.change = change
        self.dt = dt


    def change_temp(self):
        """
        Changes the value of the temperature for the current simulation based on the min and max temp possible
        """
        if self.temp >= self.maxtemp:
            self.temp += random.randint(-10 * self.dt, 0) * self.change / 10
        elif self.temp <= self.mintemp:
            self.temp += random.randint(0, 10 * self.dt) * self.change / 10
        else:
            self.temp += random.randint(-10 * self.dt , 10 * self.dt) * self.change / 10
