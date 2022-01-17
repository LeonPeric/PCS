import pygame
import form
from text import Text

width = 320*3
height = 240*3
size = [width, height]
text_color = [255, 255, 255]
background_color = [32, 32, 32]


def main():
    pygame.init()
    screen = pygame.display.set_mode(size)
    screen_center_x = screen.get_rect().centerx

    clock = pygame.time.Clock()
    clock.tick(1)

    # create background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(background_color)

    # the text itself
    welcome_text, welcome_rect = Text("Welcome to our simulation, enter your parameters here:", 32, text_color).return_object()
    welcome_rect.y = 10  # small offset to the top
    welcome_rect.centerx = screen_center_x
    background.blit(welcome_text, welcome_rect)

    screen.blit(background, [0, 0])
    # pygame.display.flip()

    # text boxes
    speed_text, speed_rect = Text("Amount of fuel", 32, text_color).return_object()
    speed_rect.y = 105
    speed_rect.x = screen_center_x - 225
    screen.blit(speed_text, speed_rect)
    speed_input = form.InputBox(screen_center_x, 100, 100, 32)
    speed_input.rect.centerx = screen_center_x
    text_boxes = [speed_input]

    # submit button
    submit_button = form.Submit("Submit", 30, 30, 100, 25, [255, 255, 255], 20)
    button, text_surface, text_rect = submit_button.return_object(screen)
    button.center = [screen.get_width()//2, screen.get_height()//2]
    text_rect.center = [button.centerx + 25, button.centery + 5]
    pygame.draw.rect(screen, [62, 62, 62], button)
    pygame.draw.rect(screen, [100, 0, 0], button, 5)
    screen.blit(text_surface, text_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            for box in text_boxes:
                box.handle_event(event)

            x, y = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if button.collidepoint(x, y):
                        screen.fill([255, 255, 255])

        for box in text_boxes:
            box.update()

        for box in text_boxes:
            box.draw(screen)

        pygame.display.flip()


main()
print(form.texts)
