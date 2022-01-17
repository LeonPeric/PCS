class Plane():
    def __init__(self, max_velocity, empty_weight, fuel, max_height, power, wing_span, thrust, takeoff_speed) -> None:
        self.max_velocity = max_velocity
        self.empty_weight = empty_weight
        self.fuel = fuel
        self.weight = self.fuel + self.empty_weight
        self.max_height = max_height
        self.power = power
        self.wing_span = wing_span
        self.thrust = thrust
        self.takeoff_speed = takeoff_speed