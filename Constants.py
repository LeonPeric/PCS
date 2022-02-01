"""
This file contains all the variables for the specific plane that we are using, a Boeing 787-9.
"""

import math

# for values see readme
DISTANCE = 5862.03*1000  # m (distance Amsterdam - New York)
SPEED = 900/3.6  # m/s max speed of a boeing
ZERO_FUEL = 181400  # KG weight of plane without fuel
FUEL = 80000  # KG weight of fuel if filled to the max
MAX_HEIGHT = 13100  # m maximum altitude of the plane
MOTOR_POWER = 7.7/(1000*1000)  # kg/N*S how much kg fuel the motor of a boeing uses per N/s
WING_SPAN = 360.5  # m2 wingspan of a boeing
C = 0.012  # air drag coefficent of subsonic transport airplane.
AIR_DENSITTY = 1.225  # kg/m^3 air density
THRUST = 360.4 * 1000 * 2  # N/s the thurst of both motors of a boeing combined
ANGLE = math.radians(15)
TAKEOFF_SPEED = 100  # m/s speed needed for takeoff
