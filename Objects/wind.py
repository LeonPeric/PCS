import random


class Wind():
    """
    Handles all the wind operations for the simulation.

    Attributes:
        Scale: int
            Scale based on the beafort wind scale in m/s.
        dt: float
            Timesteps in seconds.

    Methods:
        change_wind():
            Changes the current wind speed.
    """
    def __init__(self, scale, dt):
        """
        Constructs the wind object for the simulation.

        Parameters:
        scale: float
            Select which Beaufort parameter to use.
        dt: float
            Timesteps.
        """
        self.dt = dt
        scale += 1
        # Windspeeds according to the scale of Beaufort, reference 2
        self.Beaufort = [0, 0.2, 1.5, 3.3, 5.4, 7.9, 10.7, 13.8, 17.1, 20.7, 24.4, 28.4, 32.6, 36.8]
        self.maxspeed = self.Beaufort[scale]
        if scale > 0:
            self.minspeed = self.Beaufort[scale-1]
        else:
            self.minspeed = 0
        self.speed = random.uniform(self.minspeed, self.maxspeed)

        # the maximum change is 10% of the average speed
        self.max_acc = 0.1 * (self.maxspeed-self.minspeed)

    def change_wind(self):
        """
        Changes the wind speed by a random percantage of the max change
        It also takes timesteps into account such that bigger time steps have
        bigger changes in wind speed.
        """
        # 10 to take a random change between 0 and 10% of the maximum change
        if self.speed >= self.maxspeed:
            self.speed += random.randint(-10 * self.dt, 0) * self.max_acc / 10
        elif self.speed <= self.minspeed:
            self.speed += random.randint(0, 10 * self.dt) * self.max_acc / 10
        else:
            self.speed += random.randint(-10 * self.dt, 10 * self.dt) * self.max_acc / 10
