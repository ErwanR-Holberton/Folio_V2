import pygame
from models.tab import *
from models.drop_down_menu import drop_down_menu

PIXEL_NUMBER = 16

class main_screen():

    def __init__(self, screen):
        self.selected_tile = None
        self.coordinates = {}
        self.tile_size = 32
        self.mode = 0
        self.calculate(screen)
        pass

    def calculate(self, screen):
        self.width = screen.get_width() - tab_class.width
        height = screen.get_height()
        self.surf = pygame.Surface((self.width, height))
        if self.mode == 0:
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
        else:
            pixel_size_x = (self.width - 20) / PIXEL_NUMBER
            pixel_size_y = (height - drop_down_menu.menu_height - 20) / PIXEL_NUMBER
            pixel_size = int (min(pixel_size_x, pixel_size_y))
            offset_x = int((self.width - (pixel_size * PIXEL_NUMBER)) / 2)
            offset_y = int((height - (pixel_size * PIXEL_NUMBER) - drop_down_menu.menu_height) / 2 + drop_down_menu.menu_height)

            self.surf.fill((255, 255, 255))
            for x in range(0, (PIXEL_NUMBER + 1) * pixel_size, pixel_size):
                pygame.draw.line(self.surf, (0, 0, 0), (x + offset_x, offset_y), (x + offset_x, pixel_size * PIXEL_NUMBER + offset_y))
                pygame.draw.line(self.surf, (0, 0, 0), (offset_x, x + offset_y), (pixel_size * PIXEL_NUMBER + offset_x, x + offset_y))




    def draw(self, screen):
        screen.blit(self.surf, (0, 0))

    def click(self, x, y):
        index = "{}.{}".format(int(x/self.tile_size), int(y/self.tile_size))
        self.coordinates[index] = self.selected_tile