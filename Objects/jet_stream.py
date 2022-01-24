import random
import math
# class Jet_stream():
#     def __init__(self, scale, minspeed, maxspeed) -> None:
#         self.minspeed = minspeed
#         self.maxspeed = maxspeed
#         self.speed = random.uniform(self.minspeed, self.maxspeed)
#         self.max_acc = 0.01* scale * (self.maxspeed-self.minspeed)
    
#     def change_speed(self):
#         if self.speed >= self.maxspeed:
#             self.speed += random.randint(-10, 0) * self.max_acc / 10
#         elif self.speed <= self.minspeed:
#             self.speed += random.randint(0, 10) * self.max_acc / 10
#         else:
#             self.speed += random.randint(-10, 10) * self.max_acc / 10


class Jet_stream():
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
        self.speed =  self.constant / (self.Omega * temperature) 
