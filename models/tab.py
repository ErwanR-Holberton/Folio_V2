import pygame
from models.tab_menus import tab_menus_class

class tab_class():
    width = 300
    size_name = 50

    def __init__(self, screen):
        self.menu = []
        self.menu.append(tab_menus_class("Tiles", []))
        self.menu.append(tab_menus_class("Tools", []))
        self.menu.append(tab_menus_class("Settings", []))
        self.calculate(screen)

    def calculate(self, screen):
        font = pygame.font.Font(None, 22) #create default font size 20
        self.surf = pygame.Surface((self.width, screen.get_height()))
        self.surf.fill((250, 250, 250))

        for menu in self.menu:
            menu.draw(self.surf)
        self.draw(screen)


    def draw(self, screen):
        screen.blit(self.surf, (screen.get_width() - self.width, 0))

