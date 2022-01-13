import numpy as np
import matplotlib.pyplot as plt
# BOEING 787-9
DISTANCE = 5862.03  # km (distance Amsterdam - New York)
SPEED = 900/3600  # km/s
FUEL = 126370
ZERO_FUEL = 181400  # KG
FUEL = 80000  # KG
FUEL_USSAGE_KM = 7.18  # kg/km
FUEL_USSAGE_TIME = FUEL_USSAGE_KM*SPEED  # kg/s
MAX_HEIGHT = 13100  # m
MOTOR_POWER = (7.7 * 2)/1000  # kg/N*S
WING_SPAN = 360.5  # m2
C = 0.012  # air drag coefficent of subsonic transport airplane.
AIR_DENSITTY = 1.225  # kg/m^3
IMPULSE = 13200
THRUST = 9.81 * IMPULSE * FUEL_USSAGE_TIME
# 1. Lift (N) >= GY (N)

# KG/N
# accelateratie = N-AR/KG
# speed = prev_speed + accelaratie
# air_resistance in Newton.

# Lift (N) == GY (N)


class plane():
    def __init__(self, max_speed, empty_weight, fuel, max_height, power, wing_span, thrust) -> None:
        self.max_speed = max_speed
        self.empty_weight = empty_weight
        self.fuel = fuel
        self.weight = self.fuel + self.empty_weight
        self.max_height = max_height
        self.power = power
        self.wing_span = wing_span
        self.thrust = thrust


def calc_air_ressistance(air_density, velocity, wing_span, c):
    force = 1/2 * air_density * (velocity ** 2) * wing_span * c

    return force


def flight(plane, distance, air_density, dt=1):
    position = 0
    positionLst = [position]
    time = 0
    timeLst = [time]
    velocity = 0
    velocityLst = [velocity]
    acceleration = 0
    accelerationLst = [acceleration]
    fuelLst = [0]
    fuel_used = 0
    while position < distance and fuel_used < plane.fuel:
        time += dt
        air_ressistance = calc_air_ressistance(air_density, velocity, plane.wing_span, C)
        if velocity >= plane.max_speed:
            fuel_used += air_ressistance*plane.power
            accelerationLst.append(0)
        else:
            fuel_used += plane.thrust * plane.power
            acceleration = (plane.thrust-air_ressistance)/(plane.weight-fuel_used)
            accelerationLst.append(acceleration)
            velocity += acceleration
        velocityLst.append(velocity)
        position += velocity
        timeLst.append(time)
        positionLst.append(position)
        fuelLst.append(fuel_used)

    return timeLst, positionLst, fuelLst, accelerationLst, velocityLst


boeing = plane(max_speed=SPEED, empty_weight=ZERO_FUEL, fuel=FUEL, max_height=MAX_HEIGHT, power=MOTOR_POWER, wing_span=WING_SPAN, thrust=THRUST)
timeLst, positionLst, fuelLst, accelerationLst, velocityLst = flight(boeing, DISTANCE, AIR_DENSITTY)
print(timeLst)
print("------------------------------------------")
print(positionLst)
print("------------------------------------------")
print(fuelLst)
print("------------------------------------------")
plt.plot(timeLst, fuelLst)
plt.show()
