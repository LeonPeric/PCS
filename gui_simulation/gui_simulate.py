import sys
import pygame
import math

sys.path.insert(0, "C:\\Users\\leonp\\Documents\\UvA\\Jaar 3\\3. Project Computational Science\\PCS\\")
import airplane as plane

# variables for simulation
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

# calculate the height map for the airplane, this will be changed when the simulation works.
bottom = screen.get_height() - 100

# get the height map for the plane
flight_sim = plane.Flight(plane.boeing, plane.Wind(0), plane.DISTANCE, plane.AIR_DENSITTY)
flight_sim.run_sim(plane.ASCEND_ANGLE, plane.DESCEND_ANGLE)

max_height = max(flight_sim.heightLst)
min_height = min(flight_sim.heightLst)
height_map = [620 - (item - min_height)/(max_height - min_height) * (bottom - 100) for item in flight_sim.heightLst]
max_height = max(height_map)
min_height = min(height_map)


# main loop
def simulate_plane(height_map, screen, airplane_img, airplane_rect):
    angled = False
    airplane_rect.x = 100
    for i in range(len(height_map)):
        if i == 10:
            airplane_img = pygame.transform.rotate(airplane_img, math.degrees(plane.ASCEND_ANGLE_NOSE))
            angled = True
        elif height_map[i] == min_height:
            if angled:
                # airplane_img = pygame.transform.rotate(airplane_img, math.degrees(-plane.ASCEND_ANGLE_NOSE))
                airplane_img = backup_airplane
                angled = False
        elif height_map[i] > min_height and not angled:
            airplane_img = pygame.transform.rotate(airplane_img, math.degrees(plane.DESCEND_ANGLE_NOSE))
            angled = True

        # FPS
        if height_map[i] > min_height:
            clock.tick(100)
        elif height_map[i] == min_height:
            clock.tick(10**10)

        # set the y location of the airplane
        if angled == True:
            airplane_rect.y = height_map[i] - 50
        else:
            airplane_rect.y = height_map[i]

        # check for inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # change the value of distance traveld
        font = pygame.font.Font(None, 50)
        text = font.render(f"Distance traveled is: {round(flight_sim.positionLst[i])}", 1, (10, 10, 10))
        textpos = text.get_rect()

        # fill the screen with all the elements
        screen.fill([61, 197, 255])
        ground = pygame.Rect(0, bottom, width, 150)
        pygame.draw.rect(screen, [10, 120, 39], ground)
        screen.blit(text, textpos)
        screen.blit(airplane_img, airplane_rect)
        pygame.display.flip()


simulate_plane(height_map, screen, airplane_img, airplane_rect)
