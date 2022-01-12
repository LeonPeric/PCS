# Rocket.py
# Model of the motion of a rocket considering
# thrust caused by the burning fuel.
import math


def Rocket(velocity=15, position=11, DT=0.01, simLength=500):
    numIterations = int(simLength/DT) + 1
    acceleration_due_to_gravity = -9.81
    change_in_velocity = acceleration_due_to_gravity
    burnout_time = 60
    initial_mass = 5000
    mass = initial_mass
    massLst = [mass]
    change_in_mass = 0
    specific_impulse = 400
    change_in_velocity = -specific_impulse * acceleration_due_to_gravity * change_in_mass / mass + acceleration_due_to_gravity
    rocket_mass = 1000
    t = 0
    timeLst = [0]
    velocity = 0
    velocityLst = [velocity]
    position = 0
    positionLst = [position]
    change_in_position = velocity

    for i in range(1, numIterations):
        t = i * DT
        timeLst.append(t)
        velocity = velocity + (change_in_velocity) * DT
        velocityLst.append(velocity)
        mass = mass + (-change_in_mass) * DT
        massLst.append(mass)
        position = position + (change_in_position) * DT
        positionLst.append(position)
        if (t < burnout_time):
            change_in_mass = (initial_mass - rocket_mass)/burnout_time
        else:
            change_in_mass = 0
        change_in_velocity = -specific_impulse * acceleration_due_to_gravity * change_in_mass / mass + acceleration_due_to_gravity
        change_in_position = velocity

    return timeLst, positionLst, velocityLst, massLst
