def flight(plane, distance, air_density, dt=1):
    position = 0
    positionLst = [position]
    height = 0
    height_list = [height]
    time = 0
    timeLst = [time]
    forward_velocity = 0
    forward_velocityLst = [forward_velocity]
    upward_velocity = 0
    upward_velocityLst = [upward_velocity]
    forward_acceleration = 0
    forward_accelerationLst = [forward_acceleration]
    upward_acceleration = 0
    upward_accelerationLst = [upward_acceleration]
    fuelLst = [0]
    fuel_used = 0
    
    while position < distance and fuel_used < plane.fuel:
        time += dt
        air_ressistance = calc_air_ressistance(air_density, forward_velocity, plane.wing_span, C)
        
        
        if forward_velocity >= plane.max_speed and height >= plane.max_height:
            fuel_used += air_ressistance*plane.power
            forward_acceleration = 0
            upward_acceleration = 0
            upward_velocity = 0
        elif height >= plane.max_height:
            fuel_used += plane.thrust * plane.power
            forward_acceleration = (plane.thrust-air_ressistance)/(plane.weight-fuel_used)
            upward_acceleration = 0
            upward_velocity = 0
        elif forward_velocity >= plane.max_speed:
            lift = calc_lift(plane.ascend_angle,air_density,forward_velocity,plane.wing_span)
            forward_acceleration, upward_acceleration = calc_ascend(plane.thrust,lift,air_ressistance,plane.ascend_angle,plane.weight-fuel_used)
            forward_acceleration = 0
            if upward_acceleration < 0:
                upward_acceleration = 0
            fuel_used += plane.thrust*plane.power
        else:
            lift = calc_lift(plane.ascend_angle,air_density,forward_velocity,plane.wing_span)
            forward_acceleration, upward_acceleration = calc_ascend(plane.thrust,lift,air_ressistance,plane.ascend_angle,plane.weight-fuel_used)
            if upward_acceleration < 0:
                upward_acceleration = 0
            fuel_used += plane.thrust*plane.power
            
        forward_velocity += forward_acceleration
        upward_velocity += upward_acceleration
        height += upward_velocity
        position += forward_velocity
        forward_accelerationLst.append(forward_acceleration)
        upward_accelerationLst.append(upward_acceleration)
        forward_velocityLst.append(forward_velocity)
        upward_velocityLst.append(upward_velocity)
        timeLst.append(time)
        positionLst.append(position)
        height_list.append(height)
        fuelLst.append(fuel_used)

    return timeLst, positionLst, height_list, fuelLst, forward_accelerationLst, forward_velocityLst, upward_accelerationLst, upward_velocityLst