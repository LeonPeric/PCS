from matplotlib.style import use
import numpy as np
import matplotlib.pyplot as plt
import math
import random
from Objects.plane import Plane
from Objects.wind import Wind
from Objects.jet_stream import Jet_stream
from Objects.temperature import Temperature
from Objects.flight import Flight
import pickle

def solve_matrix(A,b):
    ATA = np.matmul(A.T, A)
    Inverse_ATA = np.linalg.inv(ATA)
    Inverse_AT = np.matmul(Inverse_ATA, A.T)
    x = np.matmul(Inverse_AT, b)

    return x



DISTANCE = 5862.03*1000  # m (distance Amsterdam - New York)
SPEED = 900/3.6  # m/s
FUEL = 126370
ZERO_FUEL = 181400  # KG
FUEL = 80000  # KG
MAX_HEIGHT = 13100  # m
MOTOR_POWER = 7.7/(1000*1000)  # kg/N*S
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
TAKEOFF_SPEED = 100 #m/s
JET_MINSPEED = 25 #m/s
JET_MAXSPEED = 100 #m/s
LATITUDE = math.radians(50)
AVG_TEMPERATURE = 221 #K
dt = 1
boeing = Plane(max_velocity=SPEED, empty_weight=ZERO_FUEL, fuel=FUEL, max_height=MAX_HEIGHT, power=MOTOR_POWER, wing_span=WING_SPAN, thrust=THRUST, takeoff_speed=TAKEOFF_SPEED)
wind = Wind(-1, dt)
temperature = Temperature(0, 0, AVG_TEMPERATURE, dt)
jet_stream = Jet_stream(LATITUDE, MAX_HEIGHT)
flight_sim = Flight(boeing, wind, jet_stream, temperature, DISTANCE, AIR_DENSITTY)
flight_sim.run_sim(ASCEND_ANGLE_NOSE, DESCEND_ANGLE)
zero_fuel_use = flight_sim.total_fuel_used

with open('used.pkl', 'rb') as f:
    usedLst = pickle.load(f)

print(np.array(usedLst).shape)
usedLst -= zero_fuel_use
usedLst_mean =np.mean(np.array(usedLst), axis=1)

A = []
for i in range(7):
    for j in range(10000):
        A.append([i**3, i**2, i , 1])
A = np.array(A)
x_all = solve_matrix(A,usedLst.flatten())

A = []
for i in range(7):
    A.append([i**3, i**2, i , 1])
A = np.array(A)

sorted_use = np.sort(usedLst)
x_min = solve_matrix(A,np.min(usedLst, axis = 1))
x_max = solve_matrix(A,np.max(usedLst, axis = 1))
x_min_99 = solve_matrix(A,sorted_use[:,100])
x_max_99 = solve_matrix(A,sorted_use[:,-100])
x_min_90 = solve_matrix(A,sorted_use[:,1000])
x_max_90 = solve_matrix(A,sorted_use[:,-1000])

plt.scatter([0,1,2,3,4,5,6], usedLst_mean)
plt.scatter([0,1,2,3,4,5,6], np.min(usedLst, axis = 1))
plt.scatter([0,1,2,3,4,5,6], np.max(usedLst, axis = 1))
plt.scatter([0,1,2,3,4,5,6], sorted_use[:,100])
plt.scatter([0,1,2,3,4,5,6], sorted_use[:,-100])
plt.scatter([0,1,2,3,4,5,6], sorted_use[:,1000])
plt.scatter([0,1,2,3,4,5,6], sorted_use[:,-1000])
plt.plot(np.matmul(A,x_all), label="pred_all")
plt.plot(np.matmul(A,x_min), label="pred_min")
plt.plot(np.matmul(A,x_max), label="pred_max")
plt.plot(np.matmul(A,x_min_99), label="pred_min_99")
plt.plot(np.matmul(A,x_max_99), label="pred_max_99")
plt.plot(np.matmul(A,x_min_90), label="pred_min_90")
plt.plot(np.matmul(A,x_max_90), label="pred_max_90")
plt.legend()
plt.show()