import numpy as np
import math


class Flight():
    """
    Creates Flight object for simulation.

    Attributes:
        plane: object
            the plane object created by the plane.py.

        wind: object
            the wind object created by wind.py.

        jet_stream: object
            the jet stream object created by jet_stream.py.

        distance: int
            distance of the flight in meters.

        air_density: int
            the air density in kg/m^3.

        C: float
            Air drag coefficient.

        dt: float
            Timestep in seconds.

    Methods:
        calc_air_ressistance():
            Calculates the current air resistance.

        calc_lift(angle):
            Calculates the current lift force.

        calc_acc_ascend(angle):
            Calculates the current acceleration of the plane while ascending.

        calc_constant_ascend(angle):
            Calculates the current ascending atributes,
            while the plane has reached max speed.

        update_lsts():
            Updates all the variables used in the simulation.

        takeoff():
            Runs the takeoff phase of the simulation.

        ascend(angle):
            Runs the ascending phase of the simulation.

        cruising_flight():
            Runs the cruising phase of the simulation.

        descend():
            Runs the descending phase of the simulation.

        landing():
            Runs the landing phase of the simulation.

        run_sim(ASCEND_ANGLE):
            Runs the simulation.
    """
    def __init__(self, plane, wind, jet_stream, distance, air_density, C=0.012, dt=1) -> None:
        self.mass = plane.weight
        self.plane = plane
        self.distance = distance
        self.air_density = air_density
        self.dt = dt
        self.drag_cov = C
        self.wind = wind
        self.jet_stream = jet_stream

        self.position = 0
        self.height = 0
        self.time = 0
        self.velocity = 0
        self.forward_velocity = 0
        self.upward_velocity = 0
        self.forward_acceleration = 0
        self.upward_acceleration = 0
        self.acceleration = 0
        self.total_fuel_used = 0

        self.positionLst = [self.position]
        self.heightLst = [self.height]
        self.timeLst = [self.time]
        self.velocityLst = [self.velocity]
        self.forward_velocityLst = [self.forward_velocity]
        self.upward_velocityLst = [self.upward_velocity]
        self.forward_accelerationLst = [self.forward_acceleration]
        self.upward_accelerationLst = [self.upward_acceleration]
        self.accelerationLst = [self.acceleration]
        self.fuelLst = [self.total_fuel_used]
        self.massLst = [self.mass]
        self.windLst = [0]
        self.jetLst = [0]

    def calc_air_ressistance(self):
        """
        Calculates the current air resistance.
        """
        force = 1/2 * self.air_density * ((self.velocity+self.wind.speed) ** 2) * self.plane.wing_span * self.drag_cov

        return force

    def calc_lift(self, angle):
        """
        Calculates the current lift force.

        Attributes:
            angle: float
                Current angle of the plane in radians.
        """
        C = 2 * math.pi * angle
        lift = 1/2 * C * self.air_density * ((self.velocity+self.wind.speed)**2) * self.plane.wing_span

        return lift

    def calc_acc_ascend(self, angle):
        """
        Calculates the current acceleration of the plane while ascending.

        Attributes:
            angle: float
                Current angle of the plane in radians.
        """

        # 9.81 because of gravity
        gravity = -self.mass * 9.81
        lift = self.calc_lift(angle)
        drag = self.calc_air_ressistance()
        thrust_forward = self.plane.thrust * math.cos(angle)
        thrust_upwards = self.plane.thrust * math.sin(angle)
        drag_forward = drag * math.cos(angle)
        drag_upwards = drag * math.sin(angle)
        forward_force = thrust_forward - drag_forward
        upward_force = gravity + lift + thrust_upwards - drag_upwards
        self.forward_acceleration = forward_force / self.mass
        self.upward_acceleration = upward_force / self.mass

    def calc_constant_ascend(self, angle):
        """
        Calculates the current ascending atributes,
        while the plane has reached max speed.

        Attributes:
            angle: float
                Current angle of the plane.
        """
        # 9.81 because of gravity
        gravity = self.mass * 9.81
        lift = -self.calc_lift(angle)
        drag = self.calc_air_ressistance()
        drag_forward = drag * math.cos(angle)
        drag_upward = drag * math.sin(angle)
        thrust_forward = drag_forward
        thrust_upwards = drag_upward + gravity + lift
        thrust = math.sqrt(thrust_upwards ** 2 + thrust_forward ** 2)

        return thrust

    def alt_calc_constant_ascend(self, angle):
        """
        Alternate methode to calculate.
        the current ascending atributes,
        while the plane has reached max speed.

        Attributes:
            angle: float
                Current angle of the plane.
        """
        # 9.81 because of gravity
        gravity = self.mass * 9.81
        lift = -self.calc_lift(angle)
        drag = self.calc_air_ressistance()
        drag_forward = drag * math.cos(angle)
        drag_upward = drag * math.sin(angle)
        thrust_forward = drag_forward
        thrust_upwards = drag_upward + gravity + lift
        thrust = math.sqrt(thrust_upwards**2 + thrust_forward**2)

        return thrust

    def update_lsts(self):
        """
        Updates all the variables used in the simulation.
        """
        self.velocityLst.append(self.velocity)
        self.heightLst.append(self.height)
        self.positionLst.append(self.position)
        self.forward_velocityLst.append(self.forward_velocity)
        self.upward_velocityLst.append(self.upward_velocity)
        self.forward_accelerationLst.append(self.forward_acceleration)
        self.upward_accelerationLst.append(self.upward_acceleration)
        self.timeLst.append(self.time)
        self.fuelLst.append(self.total_fuel_used)
        self.massLst.append(self.mass)
        self.accelerationLst.append(self.acceleration)
        self.jetLst.append(self.jet_stream.speed)
        self.windLst.append(self.wind.speed)

    def takeoff(self):
        """
        Runs the take off phase of the simulation.
        """
        while self.forward_velocity <= self.plane.takeoff_speed:
            self.time += self.dt
            self.acceleration = (self.plane.thrust - self.calc_air_ressistance()) / self.mass
            self.velocity += self.acceleration * self.dt
            self.forward_velocity = self.velocity
            fuel_used = self.plane.thrust * self.plane.power * self.dt
            self.total_fuel_used += fuel_used
            self.mass -= fuel_used
            self.position += self.forward_velocity * self.dt

            self.update_lsts()

    def ascend(self, angle):
        """
        Runs the ascending phase of the simulation.

        Attributes:
            angle: float
                angle of the plane in radians.
        """
        while self.height < self.plane.max_height:
            self.time += self.dt
            if self.velocity >= self.plane.max_velocity:
                self.upward_acceleration = 0
                self.forward_acceleration = 0
                thrust = self.calc_constant_ascend(angle)
                fuel_used = thrust * self.plane.power * self.dt
                self.total_fuel_used += fuel_used
                self.mass -= fuel_used

            else:
                self.calc_acc_ascend(angle)
                fuel_used = self.plane.thrust*self.plane.power * self.dt
                self.total_fuel_used += fuel_used
                self.mass -= fuel_used
                self.forward_velocity += self.forward_acceleration * self.dt
                self.upward_velocity = self.upward_acceleration * self.dt
                self.velocity = math.sqrt(self.forward_velocity**2 + self.upward_velocity**2)

            self.wind.change_wind()
            self.position += (self.forward_velocity - self.wind.speed) * self.dt
            self.height += self.upward_velocity * self.dt
            self.update_lsts()

    def cruising_flight(self):
        """
        Runs the cruising phase of the simulation.
        """
        self.upward_velocity = 0
        self.forward_velocity = self.velocity
        self.wind.speed = 0
        while self.position < self.distance:
            self.time += self.dt
            thrust = self.calc_air_ressistance()
            fuel_used = thrust * self.plane.power * self.dt
            self.total_fuel_used += fuel_used
            self.mass -= fuel_used
            if self.jet_stream.in_stream:
                self.position += (self.forward_velocity-self.jet_stream.speed) * self.dt
            else:
                self.position += self.forward_velocity * self.dt
            self.jet_stream.check_jet_stream(self.position)
            self.update_lsts()

    def descend(self):
        """
        Runs the descending phase of the simulation.

        NOTE: this is guesswork, this is not based on real data.
        Future work could improve this project mostly by working on this phase.
        """
        self.upward_velocity = -7
        self.forward_velocity = 150
        self.velocity = np.sqrt(7**2+150**2)
        while self.height > 0:
            self.time += self.dt
            self.height += self.upward_velocity * self.dt
            if self.height < 0:
                self.height = 0
            self.position += self.forward_velocity * self.dt
            thrust = self.calc_air_ressistance()
            fuel_used = thrust * self.plane.power * self.dt
            self.mass -= fuel_used
            self.total_fuel_used += fuel_used
            self.wind.change_wind()
            self.update_lsts()

    def landing(self):
        """
        Runs the landing phase of the simulation.

        NOTE: this is guesswork, this is not based on real data.
        Future work could improve this project mostly by working on this phase.
        But because no fuel is used in the landing phase of a flight did this not
        impact the result of the research.
        """
        self.upward_velocity = 0
        while self.forward_velocity > 0:
            self.time += self.dt
            self.forward_acceleration = -10
            self.forward_velocity += self.forward_acceleration * self.dt
            self.position += self.forward_velocity * self.dt
            self.update_lsts()

    def run_sim(self, ASCEND_ANGLE):
        """
        Runs the simulation.

        Attributes:
            ASCEND_ANGLE: float
                the ascend angle of the plane in radians.
        """
        self.takeoff()
        self.ascend(ASCEND_ANGLE)
        self.cruising_flight()
        self.descend()
        self.landing()
