class Plane():
    """
    Creates the plane object

    Attributes:
        max_velocity: float
            Max speed of the plane in m/s.
        empty_weight: int
            Weight of the plane without fuel in kg.
        fuel: int
            Amount of fuel the plane has when starting the flight in kg.
        max_height: int:
            The maximum height the plane can fly at in m.
        power: float
            How much kg of of fuel the plane uses in kg/n*s.
        WING_AREA: float
            Wing span of the plane in m^2.
        thrust: float
            Amount of thrust of the plane in n/s.
        takeoff_speed: float
            Amount of speed required to takeoff in m/s.
    """
    def __init__(self, max_velocity, empty_weight, fuel, max_height, power, WING_AREA, thrust, takeoff_speed) -> None:
        self.max_velocity = max_velocity
        self.empty_weight = empty_weight
        self.fuel = fuel
        self.weight = self.fuel + self.empty_weight
        self.max_height = max_height
        self.power = power
        self.wing_area = WING_AREA
        self.thrust = thrust
        self.takeoff_speed = takeoff_speed
