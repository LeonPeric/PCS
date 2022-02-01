import numpy as np


class Jet_stream():
    """
    Object for all jet stream related operations in the simulation.
    
    Attributes:
        average_thickness: float
            The average thickness of a jet stream in m.
        tine_diff: int
            The amount of time between jet streams in s.
        dt: float
            Timestep in second.
        scale: int
            The scale over which the values may vary from the average.

    Methods:
        check_jet_stream():
            checks wheter the jet stream should start of stop, how much time
            there is before the next jet stream, how big the new jet stream is
            and how fast the new jet stream is.
    """
    def __init__(self, average_thickness, time_diff, dt, scale=1):
        # 80 and 160 are the minimum and maximum speed of jet streams in km/h
        # 3.6 is to go from km/h to m/s
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
        # 60 to transform the scale to minutes
        self.time_till_next = np.random.normal(self.time_diff, self.scale * 60, size=None)

    def check_jet_stream(self, current_distance):
        """
        checks wheter the jet stream should start of stop, how much time
        there is before the next jet stream, how big the new jet stream is
        and how fast the new jet stream is.

        Attributes:
            current_distance: float
                the current distance of the plane in m.
        """

        # this is only for a blank run where no jet streams are active.
        if self.average_thickness == 0 and self.time_diff == 0:
            self.speed = 0

        else:
            if not self.in_stream:
                self.in_stream = self.time_since_last >= self.time_till_next
                if self.in_stream:
                    self.distance_start = current_distance
                    # 1000 to transorm the scale over kilometers
                    self.stream_thickness = np.random.normal(self.average_thickness, scale=self.scale * 1000, size=None)
                    # the difference between average and max/min speed is 10 and 1+scale to make sure the deviation is never 0.
                    self.speed = np.random.normal(self.average_speed, scale=10 - 10 / (1 + self.scale), size=None)
                else:
                    self.time_since_last += self.dt
            else:
                self.in_stream = not (current_distance - self.distance_start >= self.stream_thickness)
                if not self.in_stream:
                    self.time_since_last = 0
                    # 60 to transform the scale to minutes
                    self.time_till_next = np.random.normal(self.time_diff, scale=self.scale * 60, size=None)
