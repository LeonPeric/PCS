import numpy as np
import matplotlib.pyplot as plt
import math
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
ANGLE = math.radians(25)
TAKEOFF_SPEED = 70 #m/s
# 1. Lift (N) >= GY (N)
# KG/N
# accelateratie = N-AR/KG
# speed = prev_speed + accelaratie
# air_resistance in Newton.

# Lift (N) == GY (N)


class cl_plane():
    def __init__(self, max_velocity, empty_weight, fuel, max_height, power, wing_span, thrust, ascend_angle, takeoff_speed) -> None:
        self.max_velocity = max_velocity
        self.empty_weight = empty_weight
        self.fuel = fuel
        self.weight = self.fuel + self.empty_weight
        self.max_height = max_height
        self.power = power
        self.wing_span = wing_span
        self.thrust = thrust
        self.ascend_angle = ascend_angle
        self.takeoff_speed = takeoff_speed
        


class Flight():
    def __init__(self, plane, distance, air_density, C=0.012, dt=1) -> None:
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
        self.angle = 0
    
    
    def calc_air_ressistance(self):
        force = 1/2 * self.air_density * (self.velocity ** 2) * self.plane.wing_span * self.drag_cov

        return force
        
    
    def calc_lift(self):
        C = 2 * math.pi * self.angle #angle in radians
        lift = 1/2 * C * self.air_density * (self.velocity**2) * self.plane.wing_span

        return lift


    def calc_acc_ascend(self):
        gravity = -self.mass * 9.81
        lift = self.calc_lift()
        drag = self.calc_air_ressistance()
        thrust_forward = self.plane.thrust * math.cos(self.angle)
        thrust_upwards = self.plane.thrust * math.sin(self.angle)
        drag_forward = drag * math.cos(self.angle)
        drag_upwards = drag * math.sin(self.angle)
        forward_force = thrust_forward - drag_forward
        upward_force = gravity + lift + thrust_upwards - drag_upwards
        self.forward_acceleration = forward_force / self.mass
        self.upward_acceleration = upward_force / self.mass

        return True
    
    def calc_constant_ascend(self):
        gravity = self.mass * 9.81
        lift = -self.calc_lift()
        drag = self.calc_air_ressistance()
        drag_forward = drag * math.cos(self.angle)
        drag_upward = drag * math.sin(self.angle)
        thrust_forward = drag_forward
        thrust_upwards = drag_upward + gravity + lift
        thrust = math.sqrt(thrust_upwards ** 2 + thrust_forward ** 2)

        return thrust
        



    def update_lsts(self):
        #update lists
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
        


    def takeoff(self, ):
        while self.forward_velocity <= self.plane.takeoff_speed:
            #calculate values
            self.time += self.dt
            self.calc_acc_ascend()
            fuel_used = self.plane.thrust * self.plane.power
            self.total_fuel_used += fuel_used
            self.mass -= fuel_used
            self.forward_velocity += self.forward_acceleration
            self.position += self.forward_velocity
            self.velocity = self.forward_velocity

            self.update_lsts()

        print(self.forward_velocity)
        print("Plane has taken off!")

        return True
            
    def ascend(self, ):
        self.angle = self.plane.ascend_angle
        while self.height < self.plane.max_height:
            self.time += self.dt
            if self.velocity >= self.plane.max_velocity:
                self.upward_acceleration = 0
                self.forward_acceleration = 0
                thrust = self.calc_constant_ascend()
                fuel_used = thrust * self.plane.power
                self.total_fuel_used += fuel_used
                self.mass -= fuel_used
            
            else:
                self.calc_acc_ascend()
                fuel_used = self.plane.thrust*self.plane.power
                self.total_fuel_used += fuel_used
                self.mass -= fuel_used
                self.forward_velocity += self.forward_acceleration
                self.upward_velocity = self.upward_acceleration
                self.velocity = math.sqrt(self.forward_velocity**2 + self.upward_velocity**2)
            


            self.position += self.forward_velocity
            self.height += self.upward_velocity
            
            self.update_lsts()

        print(self.height)
        print("Ladies and gentlemen we've reached our cruising speed, you may now take off your seatbelts.")
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
            self.update_lsts()
        

        print(self.position) 
        print("We are reaching our destination, starting the descend. PUT ON YOUR SEATBELTS!")
        return True
    
    def descend(self):
        pass

    def landing(self):
        pass

    def run_sim(self):
        self.takeoff()
        self.ascend()
        self.cruising_flight()
        # self.descend()
        # self.landing()
        print(self.time)



boeing = cl_plane(max_velocity=SPEED, empty_weight=ZERO_FUEL, fuel=FUEL, max_height=MAX_HEIGHT, power=MOTOR_POWER, wing_span=WING_SPAN, thrust=THRUST, ascend_angle=ANGLE, takeoff_speed=TAKEOFF_SPEED)
#timeLst, positionLst, height_list, fuelLst, forward_accelerationLst, forward_velocityLst, upward_accelerationLst, upward_velocityLst = flight(boeing, DISTANCE, AIR_DENSITTY)
flight_sim = Flight(boeing, DISTANCE, AIR_DENSITTY)
flight_sim.run_sim()

# print(timeLst)
# print("------------------------------------------")
# print(height_list)
# print("------------------------------------------")
# print(fuelLst)
# print("------------------------------------------")
# print(positionLst)
# print("------------------------------------------")
# plt.plot(timeLst[0:50], height_list[0:50])
# plt.show()
# plt.plot(timeLst[0:50],forward_velocityLst[:50])
# plt.show()