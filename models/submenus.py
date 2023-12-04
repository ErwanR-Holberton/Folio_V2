import pygame

class submenus_class():
    def __init__(self, name):

        font = pygame.font.Font(None, 20)                           #create default font size 20
        self.text = font.render(name, True, (0, 0, 0))

        self.color = (150, 150, 150)

