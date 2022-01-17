import sys
import pygame

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
airplane = pygame.image.load("PCS/gui_simulation/data/plane_test.png")
size = airplane.get_size()
airplane = pygame.transform.flip(airplane, True, False)
airplane = pygame.transform.scale(airplane, [size[0] * SCALE_FACTOR, size[1] * SCALE_FACTOR])
airplane_rect = airplane.get_rect()

# calculate the height map for the airplane, this will be changed when the simulation works.
bottom = screen.get_height() - 100
height_map = []
fuel = int(input("How much fuel does the airplane have? "))
for i in range(fuel):
    if i < int(0.2 * fuel):
        height_map.append(bottom - (20 * i))
    elif i >= int(0.2 * fuel) and i < int(0.8 * fuel):
        height_map.append(bottom - (20 * int(0.2 * fuel)))
    elif i >= int(0.8 * fuel):
        height_map.append(bottom - (20 * (fuel - i)))
print(height_map)

# main loop
def simulate_plane(height_map, screen, airplane, airplane_rect):
    speed = 0
    distance = 0
    airplane_rect.x = 100
    for i in range(len(height_map)):
        # FPS
        clock.tick(5)

        # set the y location of the airplane
        airplane_rect.y = height_map[i]

        # check for inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # change the distance traveled and background based on it
        distance += speed
        # keep speeding up
        if distance < 100:
            if speed != 25:
                speed += 5
            color = [11, 115, 1]
        elif distance >= 100 and distance < 1000:
            color = [0, 0, 255]
        elif distance >= 1000:
            color = [11, 115, 1]

        # change the value of distance traveld
        font = pygame.font.Font(None, 50)
        text = font.render(f"Distance traveled is: {str(distance)}", 1, (10, 10, 10))
        textpos = text.get_rect()

        # fill the screen with all the elements
        screen.fill(color)
        screen.blit(text, textpos)
        screen.blit(airplane, airplane_rect)
        pygame.display.flip()


#simulate_plane(height_map, screen, airplane, airplane_rect)
