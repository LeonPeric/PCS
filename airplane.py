import numpy as np
import matplotlib.pyplot as plt
import math
import random

# BOEING 787-9
DISTANCE = 5862.03*1000  # m (distance Amsterdam - New York)
SPEED = 900/3.6  # m/s
FUEL = 126370
ZERO_FUEL = 181400  # KG
FUEL = 80000  # KG
MAX_HEIGHT = 13100  # m
MOTOR_POWER = 7.7/(1000*1000)  # g/N*S
WING_SPAN = 360.5  # m2
C = 0.012  # air drag coefficent of subsonic transport airplane.
AIR_DENSITTY = 1.225  # kg/m^3
# IMPULSE = 13200
THRUST = 360.4 * 1000 * 2 #N/s
ASCEND_ANGLE_NOSE = math.radians(15)
DESCEND_ANGLE_NOSE = math.radians(-3)
ASCEND_ANGLE_WING = math.radians(25)
DESCEND_ANGLE_WING = math.radians(-25)
ASCEND_ANGLE = (ASCEND_ANGLE_WING, ASCEND_ANGLE_NOSE)
DESCEND_ANGLE = (DESCEND_ANGLE_WING, DESCEND_ANGLE_WING)
TAKEOFF_SPEED = 80 #m/s
# 1. Lift (N) >= GY (N)
# KG/N
# accelateratie = N-AR/KG
# speed = prev_speed + accelaratie
# air_resistance in Newton.

# Lift (N) == GY (N)


class cl_plane():
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


class Flight():
    def __init__(self, plane, wind, distance, air_density, C=0.012, dt=1) -> None:
        self.position = 0
        self.positionLst = [self.position]
        self.height = 0
        self.heightLst = [self.height]
        self.time = 0
        self.timeLst = [self.time]
        self.velocity = 0
        self.velocityLst = [self.velocity]
        self.forward_velocity = 0
        self.forward_velocityLst = [self.forward_velocity]
        self.upward_velocity = 0
        self.upward_velocityLst = [self.upward_velocity]
        self.forward_acceleration = 0
        self.forward_accelerationLst = [self.forward_acceleration]
        self.upward_acceleration = 0
        self.upward_accelerationLst = [self.upward_acceleration]
        self.total_fuel_used = 0
        self.fuelLst = [self.total_fuel_used]
        self.mass = plane.weight
        self.massLst = [self.mass]
        self.plane = plane
        self.distance = distance
        self.air_density = air_density
        self.dt = dt
        self.drag_cov = C
        self.wind = wind
    
    
    def calc_air_ressistance(self):
        force = 1/2 * self.air_density * ((self.velocity-self.wind.speed) ** 2) * self.plane.wing_span * self.drag_cov

        return force
        
    
    def calc_lift(self, angle):
        C = 2 * math.pi * angle #angle in radians
        lift = 1/2 * C * self.air_density * (self.velocity**2) * self.plane.wing_span

        return lift


    def calc_acc_ascend(self, angle_nose, angle_wing):
        gravity = -self.mass * 9.81
        lift = self.calc_lift(angle_wing)
        drag = self.calc_air_ressistance()
        thrust_forward = self.plane.thrust * math.cos(angle_nose)
        thrust_upwards = self.plane.thrust * math.sin(angle_nose)
        drag_forward = drag * math.cos(angle_nose)
        drag_upwards = drag * math.sin(angle_nose)
        forward_force = thrust_forward - drag_forward
        upward_force = gravity + lift + thrust_upwards - drag_upwards
        self.forward_acceleration = forward_force / self.mass
        self.upward_acceleration = upward_force / self.mass

        return True


    def calc_constant_ascend(self, angle_nose, angle_wing):
        gravity = self.mass * 9.81
        lift = -self.calc_lift(angle_wing)
        drag = self.calc_air_ressistance()
        drag_forward = drag * math.cos(angle_nose)
        drag_upward = drag * math.sin(angle_nose)
        thrust_forward = drag_forward
        thrust_upwards = drag_upward + gravity + lift
        thrust = math.sqrt(thrust_upwards ** 2 + thrust_forward ** 2)

        return thrust
        

    def update_lsts(self):
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
        


    def takeoff(self):
        while self.forward_velocity <= self.plane.takeoff_speed:
            #calculate values
            self.time += self.dt
            self.calc_acc_ascend(0, 0)
            fuel_used = self.plane.thrust * self.plane.power
            self.total_fuel_used += fuel_used
            self.mass -= fuel_used
            self.forward_velocity += self.forward_acceleration
            self.position += self.forward_velocity
            self.velocity = self.forward_velocity

            self.update_lsts()

        # print(self.forward_velocity)
        # print("Plane has taken off!")

        return True
            
    def ascend(self, angles):
        angle_nose = angles[0]
        angle_wings = angles[1]
        while self.height < self.plane.max_height:
            self.time += self.dt
            if self.velocity >= self.plane.max_velocity:
                self.upward_acceleration = 0
                self.forward_acceleration = 0
                thrust = self.calc_constant_ascend(angle_nose, angle_wings)
                fuel_used = thrust * self.plane.power
                self.total_fuel_used += fuel_used
                self.mass -= fuel_used
            
            else:
                self.calc_acc_ascend(angle_nose, angle_wings)
                fuel_used = self.plane.thrust*self.plane.power
                self.total_fuel_used += fuel_used
                self.mass -= fuel_used
                self.forward_velocity += self.forward_acceleration
                self.upward_velocity = self.upward_acceleration
                self.velocity = math.sqrt(self.forward_velocity**2 + self.upward_velocity**2)
            
            self.wind.change_wind()
            self.position += self.forward_velocity
            self.height += self.upward_velocity
            
            self.update_lsts()

        # print(self.height)
        # print("Ladies and gentlemen we've reached our cruising speed, you may now take off your seatbelts.")
        return True

    def cruising_flight(self):
        self.upward_velocity = 0
        self.forward_velocity = self.velocity
        while self.position < self.distance:
            self.time += self.dt
            thrust = self.calc_air_ressistance()
            fuel_used = thrust * self.plane.power
            self.total_fuel_used += fuel_used
            self.mass -= fuel_used
            self.position += self.forward_velocity
            self.wind.change_wind()
            self.update_lsts()
        

        # print(self.position) 
        # print("We are reaching our destination, starting the descend. PUT ON YOUR SEATBELTS!")
        return True
    
    def descend(self):
        self.upward_velocity = -7
        self.forward_velocity = 150
        self.velocity = np.sqrt(7**2+150**2)
        while self.height > 0:
            self.time += self.dt
            self.height += self.upward_velocity
            if self.height < 0:
                self.height = 0
            self.position += self.forward_velocity
            thrust = self.calc_air_ressistance()
            fuel_used = thrust * self.plane.power
            self.mass -= fuel_used
            self.total_fuel_used += fuel_used
            self.wind.change_wind()
            self.update_lsts()

        # print(self.height)
        # print("We reached ground level, BRACE FOR IMPACT")
        return True
    def landing(self):
        self.upward_velocity = 0
        while self.forward_velocity > 0:
            self.time += self.dt
            self.forward_acceleration = -10
            self.forward_velocity += self.forward_acceleration
            self.position += self.forward_velocity
            self.update_lsts()
        
        # print(self.forward_velocity)
        # print("We've landed thank you for flying with Amigos and Airlines")
        
        return True
        
    def run_sim(self, ASCEND_ANGLE, DESCEND_ANGLE):
        self.takeoff()
        self.ascend(ASCEND_ANGLE)
        self.cruising_flight()
        self.descend()
        self.landing()
        # print(self.time)

boeing = cl_plane(max_velocity=SPEED, empty_weight=ZERO_FUEL, fuel=FUEL, max_height=MAX_HEIGHT, power=MOTOR_POWER, wing_span=WING_SPAN, thrust=THRUST, takeoff_speed=TAKEOFF_SPEED)

usedLst = []
wind = Wind(0)
flight_sim = Flight(boeing, wind, DISTANCE, AIR_DENSITTY)
flight_sim.run_sim(ASCEND_ANGLE, DESCEND_ANGLE)
fuel_no_wind = flight_sim.total_fuel_used
for i in range(1,14):
    print(i)
    used = 0
    for j in range(10):
        wind = Wind(i)
        #timeLst, positionLst, height_list, fuelLst, forward_accelerationLst, forward_velocityLst, upward_accelerationLst, upward_velocityLst = flight(boeing, DISTANCE, AIR_DENSITTY)
        flight_sim = Flight(boeing, wind, DISTANCE, AIR_DENSITTY)
        flight_sim.run_sim(ASCEND_ANGLE, DESCEND_ANGLE)
        #plt.plot(flight_sim.timeLst, flight_sim.fuelLst, label=f"Windkracht: {i}")
        used += flight_sim.total_fuel_used
    mean = used/10
    usedLst.append(mean)

diff_0 = []
for i in range(13):
    average_fuel = usedLst[i]
    difference = (average_fuel/fuel_no_wind-1)*100
    diff_0.append(difference)
bars = [f"Windkracht: {i}" for i in range(13)]
plt.bar([i for i in range(13)], diff_0)
plt.xticks([i for i in range(13)], bars)
plt.show()


# print(timeLst)
# print("------------------------------------------")
# print(height_list)
# print("------------------------------------------")
# print(fuelLst)
# print("------------------------------------------")
# print(positionLst)
# # print("------------------------------------------")
# plt.plot(flight_sim.timeLst, flight_sim.fuelLst)
# plt.show()
# plt.plot(timeLst[0:50],forward_velocityLst[:50])
# plt.show()