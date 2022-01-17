import pygame


class Text:
    def __init__(self, text, size, text_color):
        font = pygame.font.Font(None, size)
        self.text = font.render(text, True, text_color)
        self.text_position = self.text.get_rect()

    def return_object(self):
        return self.text, self.text_position
