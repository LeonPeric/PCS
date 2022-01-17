import random

class Wind():
    def __init__(self, scale) -> None:
        self.Beaufort = [0, 0.2, 1.5, 3.3, 5.4, 7.9, 10.7, 13.8, 17.1, 20.7, 24.4, 28.4, 32.6, 36.8]
        self.maxspeed = self.Beaufort[scale]
        self.speed = random.uniform(-self.maxspeed, 0)
        self.max_acc = 0.1 * self.maxspeed
    
    def change_wind(self):
        if self.speed >= 0:
            self.speed += random.randint(-10, 0) * self.max_acc / 10
        elif self.speed <= -self.maxspeed:
            self.speed += random.randint(0, 10) * self.max_acc / 10
        else:
            self.speed += random.randint(-10, 10) * self.max_acc / 10