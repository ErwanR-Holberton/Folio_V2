import pygame
from models.tab import *

PIXEL_NUMBER = 16

class main_screen():

    def __init__(self, screen):
        """Initialize the main screen instance"""
        self.selected_tile = None # Currently selected tile
        self.coordinates = {} # Dictionary to store coordinates and corresponding tiles
        self.tile_size = 32 # Size of each tile
        self.mode = 0 # Display mode (0 for map grid, 1 for tile grid)
        self.calculate(screen) # Calculate the initial state of the main screen
        pass

    def calculate(self, screen):
        """Calculate the appearance of the main screen based on the current mode"""

        self.width = screen.get_width() - tab_class.width
        height = screen.get_height()
        self.surf = pygame.Surface((self.width, height))

        if self.mode == 0:
            """Map grid mode"""
            self.surf.fill((54, 57, 63)) # Background color
            for x in range(0, self.width, self.tile_size):
                pygame.draw.line(self.surf, (0, 0, 0), (x, 0), (x, height)) # Vertical grid lines
            for y in range(0, height, self.tile_size):
                pygame.draw.line(self.surf, (0, 0, 0), (0, y), (self.width, y)) # Horizontal grid lines
            for key, value in self.coordinates.items():
                key = key.split(".")
                x = int(key[0])
                y = int(key[1])
                if self.selected_tile is not None:
                    self.surf.blit(value, (x * self.tile_size, y * self.tile_size))
        else:
            """ Tile grid mode"""
            pixel_size_x = (self.width - 20) / PIXEL_NUMBER
            pixel_size_y = (height - 30 - 20) / PIXEL_NUMBER #remplacer 30 par menu height
            pixel_size = int (min(pixel_size_x, pixel_size_y))
            offset_x = int((self.width - (pixel_size * PIXEL_NUMBER)) / 2)
            offset_y = int((height - (pixel_size * PIXEL_NUMBER) - 30) / 2 + 30) #remplacer 30 par menu height

            self.surf.fill((255, 255, 255)) # Background color
            for x in range(0, (PIXEL_NUMBER + 1) * pixel_size, pixel_size):
                pygame.draw.line(self.surf, (0, 0, 0), (x + offset_x, offset_y), (x + offset_x, pixel_size * PIXEL_NUMBER + offset_y))
                pygame.draw.line(self.surf, (0, 0, 0), (offset_x, x + offset_y), (pixel_size * PIXEL_NUMBER + offset_x, x + offset_y))


    def draw(self, screen):
        """Draw the main screen on the given screen surface"""

        screen.blit(self.surf, (0, 0))

    def click(self, x, y):
        """Handle a click event on the main screen"""

        if self.selected_tile is None:
            return
        index = "{}.{}".format(int(x/self.tile_size), int(y/self.tile_size))
        self.coordinates[index] = self.selected_tile
