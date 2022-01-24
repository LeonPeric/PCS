import sys
import pygame
import math

sys.path.insert(0, "C:\\Users\\leonp\\Documents\\UvA\\Jaar 3\\3. Project Computational Science\\PCS\\")
from Objects.plane import Plane
from Objects.wind import Wind
from Objects.jet_stream import Jet_stream
from Objects.temperature import Temperature
from Objects.flight import Flight

# DISTANCE = 5862.03*1000  # m (distance Amsterdam - New York)
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
THRUST = 360.4 * 1000 * 2  # N/s
ASCEND_ANGLE_NOSE = math.radians(15)
DESCEND_ANGLE_NOSE = math.radians(-3)
ASCEND_ANGLE_WING = math.radians(25)
DESCEND_ANGLE_WING = math.radians(-25)
ASCEND_ANGLE = (ASCEND_ANGLE_WING, ASCEND_ANGLE_NOSE)
DESCEND_ANGLE = (DESCEND_ANGLE_WING, DESCEND_ANGLE_WING)
TAKEOFF_SPEED = 100  # m/s
JET_MINSPEED = 25  # m/s
JET_MAXSPEED = 100  # m/s
LATITUDE = math.radians(50)
AVG_TEMPERATURE = 221  # K
dt = 1

# variables for screen
width = 320*3
height = 240*3
size = [width, height]
SCALE_FACTOR = 0.5

# initialize the game
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)

# load the airplane and rescale it
airplane_img = pygame.image.load("PCS/gui_simulation/data/plane_test.png")
size = airplane_img.get_size()
airplane_img = pygame.transform.flip(airplane_img, True, False)
airplane_img = pygame.transform.scale(airplane_img, [size[0] * SCALE_FACTOR, size[1] * SCALE_FACTOR]).convert_alpha()
backup_airplane = airplane_img.copy()
airplane_rect = airplane_img.get_rect()

bottom = screen.get_height() - 100

# get the height map for the plane
boeing = Plane(max_velocity=SPEED, empty_weight=ZERO_FUEL, fuel=FUEL, max_height=MAX_HEIGHT, power=MOTOR_POWER, wing_span=WING_SPAN, thrust=THRUST, takeoff_speed=TAKEOFF_SPEED)
wind = Wind(-1, dt)
temperature = Temperature(0, 0, AVG_TEMPERATURE, dt)
jet_stream = Jet_stream(LATITUDE, MAX_HEIGHT)
flight_sim = Flight(boeing, wind, jet_stream, temperature, DISTANCE, AIR_DENSITTY)
flight_sim.run_sim(ASCEND_ANGLE_NOSE, DESCEND_ANGLE)

max_height = max(flight_sim.heightLst)
min_height = min(flight_sim.heightLst)
# normalize the height map values to the correct pixel coordinates
height_map = [bottom - (item - min_height)/(max_height - min_height) * (bottom - 100) for item in flight_sim.heightLst]
max_height = max(height_map)
min_height = min(height_map)


# main loop
def simulate_plane(height_map, screen, airplane_img, airplane_rect):
    angled = False
    airplane_rect.x = 100
    for i in range(len(height_map)):
        if i == 10:
            airplane_img = pygame.transform.rotate(airplane_img, math.degrees(ASCEND_ANGLE_NOSE))
            angled = True
        elif height_map[i] == min_height:
            if angled:
                airplane_img = backup_airplane.copy()
                angled = False
        elif height_map[i] > min_height and not angled:
            airplane_img = pygame.transform.rotate(airplane_img, math.degrees(DESCEND_ANGLE_NOSE))
            angled = True
        elif i > 100 and height_map[i] == bottom:
            airplane_img = backup_airplane

        # FPS
        if height_map[i] > min_height:
            clock.tick(50)
        elif height_map[i] == min_height:
            clock.tick(10**10)

        # set the y location of the airplane
        if angled:
            airplane_rect.y = height_map[i] - 50
        else:
            airplane_rect.y = height_map[i]

        # check for inputs

        # change the value of distance traveld
        font = pygame.font.Font(None, 40)
        distance_text = font.render(f"Distance traveled is: {round(flight_sim.positionLst[i] / 1000)} km of total {DISTANCE/1000}", 1, (10, 10, 10))
        distance_textpos = distance_text.get_rect()

        speed_text = font.render(f"Current velocity: {round(flight_sim.velocityLst[i])}", 1, (10, 10, 10))
        speed_textpos = speed_text.get_rect()
        speed_textpos.update(0, 30, 100, 50)

        fuel_text = font.render(f"| Fuel used in KG: {round(flight_sim.fuelLst[i])}", 1, (10, 10, 10))
        fuel_textpos = fuel_text.get_rect()
        fuel_textpos.update(375, 30, 100, 50)

        time_text = font.render(f"Time passed: {round(flight_sim.timeLst[i]/60/60, 2)} hours", 1, (10, 10, 10))
        time_textpos = time_text.get_rect()
        time_textpos.update(0, 60, 100, 50)

        if angled:
            wind_jetstream_text = font.render(f"The wind speed is currently: {flight_sim.windLst[i]}", 1, (10, 10, 10))
        else:
            wind_jetstream_text = font.render(f"The jet stream is currently: {flight_sim.jetLst[i]}", 1, (10, 10, 10))
        wind_jetstream_textpos = wind_jetstream_text.get_rect()
        wind_jetstream_textpos.update(375, 60, 100, 50)

        # fill the screen with all the elements

        if i <= len(height_map):
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                screen.fill([61, 197, 255])

                ground = pygame.Rect(0, bottom, width, 150)
                if flight_sim.positionLst[i] < 24000:
                    pygame.draw.rect(screen, [10, 120, 39], ground)
                elif flight_sim.positionLst[i] >= 24000 and flight_sim.positionLst[i] < DISTANCE - 200000:
                    pygame.draw.rect(screen, [11, 19, 163], ground)
                elif flight_sim.positionLst[i] >= DISTANCE - 200000:
                    pygame.draw.rect(screen, [10, 120, 39], ground)

                screen.blit(distance_text, distance_textpos)
                screen.blit(speed_text, speed_textpos)
                screen.blit(fuel_text, fuel_textpos)
                screen.blit(time_text, time_textpos)
                screen.blit(airplane_img, airplane_rect)
                screen.blit(wind_jetstream_text, wind_jetstream_textpos)

                pygame.display.flip()
                if i < len(height_map) - 1:
                    break


simulate_plane(height_map, screen, airplane_img, airplane_rect)
