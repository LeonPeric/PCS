"""
This file contains all the variables for the specific plane that we are using, a Boeing 787-9.
"""

import math

# for values see readme
DISTANCE = 5862.03*1000  # m (distance Amsterdam - New York)
TAKEOFF_SPEED = 100  # m/s speed needed for takeoff

# see reference 2 and 3
SPEED = 1100/3.6  # m/s max speed of the plane
ZERO_FUEL = 170000  # KG weight of the plane without fuel
FUEL = 80000  # KG weight of fuel if filled to the max
MAX_HEIGHT = 13100  # m maximum altitude of the plane
MOTOR_POWER = 7.7/(1000*1000)  # kg/N*S how much kg fuel the motor of the plane uses per N/s
WING_SPAN = 60.1218  # m wingspan of the plane
WING_CHORD = 6.27126  # mean wing chord of the plane
WING_AREA = WING_SPAN * WING_CHORD
ANGLE = math.radians(15)  # angle of attack
THRUST = 330 * 1000 * 2  # N/s the thrust of both motors of the plane combined

# see reference 1
C = 0.024  # air drag coefficent of a boeing 787

# see reference 7
AIR_DENSITTY = 1.225  # kg/m^3 air density
