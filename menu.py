"""Menu for game"""

import pygame

SCREEN_HEIGHT = 1280
SCREEN_WIDTH = 720

screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
pygame.display.set_caption('Game Menu')

# loading button Icons
button_1_image = pygame.image.load('smily.png')
button_2_image = pygame.image.load('notsmily.png')


class Button:
    """Button class for pygame."""
    def __init__(self, x, y, icon, scale_key) -> None:
        scaled_width = icon.get_width()
        scaled_height = icon.get_height()
        self.icon = pygame.transform.scale(icon, (int(scaled_width * scale_key), (int(scaled_height * scale_key))))
        self.x = x
        self.y = y
        self.rect = self.icon.get_rect()
        self.rect.topright = (x, y)

    def draw(self) -> None:
        """draw the Button"""
        position = pygame.mouse.get_pos()

       # if self.rect.topright[0] >=


        screen.blit(self.icon, (self.rect.x, self.rect.y))


button_1_run = Button(500, 200, button_1_image, scale_key=2)
button_2_run = Button(900, 200, button_2_image, scale_key=2)

# loop to run menu
current = True
while current:
    # fill screen colour
    screen.fill((205, 133, 63))

    button_1_run.draw()
    button_2_run.draw()
    # event handler
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            current = False
    pygame.display.update()

pygame.quit()
