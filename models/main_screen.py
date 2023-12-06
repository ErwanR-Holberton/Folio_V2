import pygame
from models.tab_menus import *

class main_screen():
    def __init__(self, screen):
        self.coordinates = {}
        self.tile_size = 32
        self.calculate(screen)
        pass

    def calculate(self, screen):
        width = screen.get_width() - tab_menu_class.width
        height = screen.get_height()
        self.surf = pygame.Surface((width, height))
        self.surf.fill((54, 57, 63))
        for x in range(0, width, self.tile_size):
            pygame.draw.line(self.surf, (0, 0, 0), (x, 0), (x, height))
        for y in range(0, height, self.tile_size):
            pygame.draw.line(self.surf, (0, 0, 0), (0, y), (width, y))
        for key, value in self.coordinates.items():
            key = key.split(".")
            x = int(key[0])
            y = int(key[1])
            if value == 1:
                pygame.draw.rect(self.surf, (50, 50, 50), (x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size))

    def draw(self, screen):
        screen.blit(self.surf, (0, 0))

    def click(self, x, y):
        index = "{}.{}".format(int(x/self.tile_size), int(y/self.tile_size))
        self.coordinates[index] = 1