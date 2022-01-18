import random
import numpy as np

class Temperature():
    def __init__(self, scale, change, avg_temp) -> None:
        self.temp = np.random.normal(avg_temp,scale, size=None)
        self.mintemp = avg_temp - 3 * scale
        self.maxtemp = avg_temp + 3 * scale
        self.change = change


    def change_temp(self):
        if self.temp >= self.maxtemp:
            self.temp += random.randint(-10, 0) * self.change / 10
        elif self.temp <= self.mintemp:
            self.temp += random.randint(0, 10) * self.change / 10
        else:
            self.temp += random.randint(-10, 10) * self.change / 10
