import numpy as np
import matplotlib.pyplot as plt
import math
import random
from Objects.plane import Plane
from Objects.wind import Wind
from Objects.jet_stream import Jet_stream
from Objects.temperature import Temperature


class Flight():
    def __init__(self, plane, wind, jet_stream, temperature, distance, air_density, C=0.012, dt=1) -> None:
        self.mass = plane.weight
        self.plane = plane
        self.distance = distance
        self.air_density = air_density
        self.dt = dt
        self.drag_cov = C
        self.wind = wind
        self.jet_stream = jet_stream
        self.temperature = temperature
        
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
        self.force_angle = 0
        self.velocity_anlge = 0
        
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

    
    def calc_air_ressistance(self):
        force = 1/2 * self.air_density * ((self.velocity+self.wind.speed) ** 2) * self.plane.wing_span * self.drag_cov

        return force
        
    
    def calc_lift(self, angle):
        C = 2 * math.pi * angle #angle in radians
        lift = 1/2 * C * self.air_density * ((self.velocity+self.wind.speed)**2) * self.plane.wing_span

        return lift


    # def calc_speed(self):
    #     old_speed = self.velocity
    #     print('--------------------------------------------------')
    #     print(self.force_angle)
    #     print(self.velocity_anlge)
    #     angle_force_velocity = abs(self.force_angle - self.velocity_anlge)
    #     print(angle_force_velocity)
        
    #     if angle_force_velocity != 0:
    #         new_speed = np.sqrt(old_speed ** 2 + self.acceleration ** 2 - 2 * old_speed * self.acceleration * math.cos(math.radians(180) - angle_force_velocity))
    #         new_angle = math.acos((self.acceleration ** 2 - old_speed ** 2 - new_speed ** 2 ) / (-2 * old_speed * new_speed ))
    #         print(new_angle)
    #     else:
    #         new_speed = self.velocity+self.acceleration
    #         new_angle = 0
    #     self.velocity = new_speed
    #     self.velocity_anlge += new_angle
    #     self.forward_velocity = self.velocity * math.cos(self.velocity_anlge)
    #     self.upward_velocity = self.velocity * math.sin(self.velocity_anlge)
    #     print('--------------------------------------------')
    #     return True

   
    
    # def calc_acc_ascend(self,angle_nose):
    #     gravity = -self.mass * 9.91
    #     lift = self.calc_lift(angle_nose)
    #     drag = - self.calc_air_ressistance()
    #     thrust = self.plane.thrust
    #     lift_x = - lift * math.cos(math.radians(90) - angle_nose)
    #     lift_y = lift * math.sin(math.radians(90) - angle_nose)
    #     thrust = thrust+drag
    #     thrust_x = thrust * math.cos(angle_nose)
    #     thrust_y = thrust * math.sin(angle_nose)

    #     force_x = thrust_x + lift_x
    #     force_y = gravity + lift_y + thrust_y
    #     # print(f"gravity: {gravity}")
    #     # print(f"lift: {lift_x, lift_y}")
    #     # print(f"thrust: {thrust_x, thrust_y}")
    #     # print(f"force_y: {force_y}")
    #     # print(f"force_x: {force_x}")
    #     self.upward_acceleration = force_y / self.mass
    #     self.forward_acceleration = force_x / self.mass
    #     return True

    # def calc_constant_ascend(self, angle_nose):
    #     gravity = self.mass * 9.91
    #     lift = self.calc_lift(angle_nose)
    #     drag = self.calc_air_ressistance()
    #     lift_x = lift * math.cos(math.radians(90) - angle_nose)
    #     lift_y = lift * math.sin(math.radians(90) - angle_nose)
    #     drag_x = drag * math.cos(angle_nose)
    #     drag_y = drag * math.sin(angle_nose)
    #     force_x = lift_x + drag_x
    #     force_y = lift_y - gravity - drag_y

    #     thrust_x = force_x
    #     thrust_y = -force_y

    #     thrust = math.sqrt((thrust_x ** 2) + (thrust_y**2) )

    #     return thrust

    def calc_acc_ascend(self, angle):
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

        return True
    
    def calc_constant_ascend(self, angle):
        gravity = self.mass * 9.81
        lift = -self.calc_lift(angle)
        drag = self.calc_air_ressistance()
        drag_forward = drag * math.cos(angle)
        drag_upward = drag * math.sin(angle)
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
        self.accelerationLst.append(self.acceleration)
        

    def takeoff(self):
        while self.forward_velocity <= self.plane.takeoff_speed:
            #calculate values
            self.time += self.dt
            self.acceleration = (self.plane.thrust - self.calc_air_ressistance()) / self.mass
            self.velocity += self.acceleration
            self.forward_velocity = self.velocity
            fuel_used = self.plane.thrust * self.plane.power
            self.total_fuel_used += fuel_used
            self.mass -= fuel_used
            self.position += self.forward_velocity

            self.update_lsts()

        print(self.forward_velocity)
        print("Plane has taken off!")

        return True


    def ascend(self, angle):
        while self.height < self.plane.max_height:
            self.time += self.dt
            if self.velocity >= self.plane.max_velocity:
                self.upward_acceleration = 0
                self.forward_acceleration = 0
                thrust = self.calc_constant_ascend(angle)
                fuel_used = thrust * self.plane.power
                self.total_fuel_used += fuel_used
                self.mass -= fuel_used
            
            else:
                self.calc_acc_ascend(angle)
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

    def alt_ascend(self):
        while self.height < self.plane.max_height:
            self.time += self.dt
            self.calc_acc_ascend(0)
            # time_zero = self.upward_velocity/-self.upward_acceleration
            # height_descent = self.height + 1/2 * self.upward_velocity * time_zero
            # print(time_zero)
            # print(height_descent)
            if self.velocity >= self.plane.max_velocity :
                self.forward_acceleration = 0
                self.upward_acceleration = 0
                thrust = self.calc_constant_ascend(angle_nose)
                fuel_used = thrust * self.plane.power
                self.total_fuel_used += fuel_used
                self.mass -= fuel_used
            
            else:
                self.calc_acc_ascend(angle_nose)
                fuel_used = self.plane.thrust*self.plane.power
                self.total_fuel_used += fuel_used
                self.mass -= fuel_used
                self.forward_velocity += self.forward_acceleration
                self.upward_velocity += self.upward_acceleration
                self.velocity = math.sqrt((self.forward_velocity ** 2) + (self.upward_velocity ** 2))
            # break

            # else:
            #     print('else')
            #     self.calc_acc_ascend(0)
            #     fuel_used = self.plane.thrust*self.plane.power
            #     self.total_fuel_used += fuel_used
            #     self.mass -= fuel_used
            #     self.forward_velocity -= self.upward_acceleration
            #     self.upward_velocity += self.upward_acceleration
            #     # self.velocity = math.sqrt((self.forward_velocity ** 2) + (self.upward_velocity ** 2))
            
            #     print('------------------------------------')
            #     print("fa", self.forward_acceleration)
            #     print("ua", self.upward_acceleration)
            #     print("fv", self.forward_velocity)
            #     print("uv", self.upward_velocity)
            #     print("pos", self.position)
            #     print("height",self.height)
            #     print('-------------------------------------------------------')
            # break
            self.wind.change_wind()
            self.position += self.forward_velocity
            self.height += self.upward_velocity
            
            self.update_lsts()

        print(self.height)
        print("Ladies and gentlemen we've reached our cruising speed, you may now take off your seatbelts.")
        return True


    def cruising_flight(self):
        self.upward_velocity = 0
        self.forward_velocity = self.velocity
        self.wind.speed = 0
        while self.position < self.distance:
            self.time += self.dt
            self.jet_stream.calc_speed(self.temperature.temp)
            thrust = self.calc_air_ressistance()
            fuel_used = thrust * self.plane.power
            self.total_fuel_used += fuel_used
            self.mass -= fuel_used
            self.position += self.forward_velocity-self.jet_stream.speed
            self.temperature.change_temp()
            self.update_lsts()
        

        print(self.position) 
        print("We are reaching our destination, starting the descend. PUT ON YOUR SEATBELTS!")
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

        print(self.height)
        print("We reached ground level, BRACE FOR IMPACT")
        return True


    def landing(self):
        self.upward_velocity = 0
        while self.forward_velocity > 0:
            self.time += self.dt
            self.forward_acceleration = -10
            self.forward_velocity += self.forward_acceleration
            self.position += self.forward_velocity
            self.update_lsts()
        
        print(self.forward_velocity)
        print("We've landed thank you for flying with Amigos and Airlines")
        
        return True
        

    def run_sim(self, ASCEND_ANGLE, DESCEND_ANGLE):
        self.takeoff()
        self.ascend(ASCEND_ANGLE)
        self.cruising_flight()
        self.descend()
        self.landing()
        # print(self.time)


# def test_wind(plane):




def main():
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
    TAKEOFF_SPEED = 100 #m/s
    JET_MINSPEED = 25 #m/s
    JET_MAXSPEED = 100 #m/s
    LATITUDE = math.radians(50)
    AVG_TEMPERATURE = 221 #K

    
    boeing = Plane(max_velocity=SPEED, empty_weight=ZERO_FUEL, fuel=FUEL, max_height=MAX_HEIGHT, power=MOTOR_POWER, wing_span=WING_SPAN, thrust=THRUST, takeoff_speed=TAKEOFF_SPEED)
    wind = Wind(-1)
    temperature = Temperature(0, 0, AVG_TEMPERATURE)
    jet_stream = Jet_stream(LATITUDE, MAX_HEIGHT)
    flight_sim = Flight(boeing, wind, jet_stream, temperature, DISTANCE, AIR_DENSITTY)
    flight_sim.run_sim(ASCEND_ANGLE_NOSE, DESCEND_ANGLE)
    # print(flight_sim.timeLst)
    # print(flight_sim.heightLst)
    # print(flight_sim.positionLst)
    plt.plot(flight_sim.timeLst, flight_sim.upward_velocityLst)
    plt.show()
    # usedLst = []
    # wind = Wind(-1)
    # # wind = Wind(-1)
    # # jet_stream = Jet_stream(0, JET_MINSPEED, JET_MAXSPEED)
    # for i in range(1,10):
    #     print(i)
    #     used = []
    #     for j in range(10):
    #         temperature = Temperature(i, 0, AVG_TEMPERATURE)
    #         jet_stream = Jet_stream(LATITUDE, MAX_HEIGHT)
    #         flight_sim = Flight(boeing, wind, jet_stream, temperature, DISTANCE, AIR_DENSITTY)
    #         flight_sim.run_sim(ASCEND_ANGLE, DESCEND_ANGLE)
    #         #plt.plot(flight_sim.timeLst, flight_sim.fuelLst, label=f"Windkracht: {i}")
    #         used.append(flight_sim.total_fuel_used)
    #     usedLst.append(used)



    # fig, axs = plt.subplots(2, figsize=(25,50))
    # bars = [f"Scale: {i}" for i in range(1,10)]
    # # print(usedLst)
    # vp_1 = axs[0].violinplot(usedLst, [i*2 for i in range(9)], widths=2, showmeans=True, showmedians=False, showextrema=False)
    # axs[0].set_xticks([i*2 for i in range(9)])
    # axs[0].set_xticklabels(bars)
    # axs[0].title.set_text("Effect of standard deviantion of temperature on fuel use")
    # # plt.violinplot([i for i in range(10)], usedLst)
    # # plt.xticks([i for i in range(10)], bars)
    
    # usedLst = []
    # for i in range(1,10):
    #     print(i)
    #     used = []
    #     for j in range(10):
    #         temperature = Temperature(5, i/100, AVG_TEMPERATURE)
    #         jet_stream = Jet_stream(LATITUDE, MAX_HEIGHT)
    #         flight_sim = Flight(boeing, wind, jet_stream, temperature, DISTANCE, AIR_DENSITTY)
    #         flight_sim.run_sim(ASCEND_ANGLE, DESCEND_ANGLE)
    #         used.append(flight_sim.total_fuel_used)
    #     usedLst.append(used)
    
    # bars = [f"Change: {i}" for i in range(1,10)]
    # vp_2 = axs[1].violinplot(usedLst, [i*2 for i in range(9)], widths=2, showmeans=True, showmedians=False, showextrema=False)
    # axs[1].set_xticks([i*2 for i in range(9)])
    # axs[1].set_xticklabels(bars)
    # axs[1].title.set_text("Effect of more random change of temperature on fuel use") 
    # plt.show()

    # print(timeLst)
    # print("------------------------------------------")
    # print(height_list)
    # print("------------------------------------------")
    # print(fuelLst)
    # print("------------------------------------------")
    # print(positionLst)
    # # print("------------------------------------------")
    # wind = Wind(4)
    # flight_sim = Flight(boeing, wind, DISTANCE, AIR_DENSITTY)
    # flight_sim.run_sim(ASCEND_ANGLE, DESCEND_ANGLE)
    # plt.plot(flight_sim.timeLst, flight_sim.fuelLst)
    # plt.show()
    # plt.plot(timeLst[0:50],forward_velocityLst[:50])
    # plt.show()

    return True

if __name__ == "__main__":
    main()

