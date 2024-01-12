import pygame
from models.tab import *

class main_screen():

    def __init__(self, screen):
        self.selected_tile = None
        self.coordinates = {}
        self.tile_size = 32
        self.calculate(screen)
        pass

    def calculate(self, screen):
        self.width = screen.get_width() - tab_class.width
        height = screen.get_height()
        self.surf = pygame.Surface((self.width, height))
        self.surf.fill((54, 57, 63))
        for x in range(0, self.width, self.tile_size):
            pygame.draw.line(self.surf, (0, 0, 0), (x, 0), (x, height))
        for y in range(0, height, self.tile_size):
            pygame.draw.line(self.surf, (0, 0, 0), (0, y), (self.width, y))
        for key, value in self.coordinates.items():
            key = key.split(".")
            x = int(key[0])
            y = int(key[1])
            if self.selected_tile is not None:
                self.surf.blit(value, (x * self.tile_size, y * self.tile_size))

    def draw(self, screen):
        screen.blit(self.surf, (0, 0))

    def click(self, x, y):
        index = "{}.{}".format(int(x/self.tile_size), int(y/self.tile_size))
        self.coordinates[index] = self.selected_tile