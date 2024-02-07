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
        self.tile_grid = [[(0, 255, 255) for value in range(16)] for value in range(16)]
        self.offset = (0, 0)

        self.calculate(screen) # Calculate the initial state of the main screen

    def calculate(self, screen, offset = None):
        """Calculate the appearance of the main screen based on the current mode"""

        if offset != None:
            self.offset = offset
        else:
            offset = self.offset
        self.width = screen.get_width() - tab_class.width
        height = screen.get_height()
        self.surf = pygame.Surface((self.width, height))

        if self.mode == 0:
            """Map grid mode"""
            self.surf.fill((54, 57, 63)) # Background color
            dx = offset[0] % self.tile_size
            dy = offset[1] % self.tile_size
            for x in range(0, self.width, self.tile_size):
                pygame.draw.line(self.surf, (0, 0, 0), (x + dx, 0), (x + dx, height)) # Vertical grid lines
            for y in range(0, height, self.tile_size):
                pygame.draw.line(self.surf, (0, 0, 0), (0, y + dy), (self.width, y + dy)) # Horizontal grid lines
            for key, value in self.coordinates.items():
                key = key.split(".")
                x = int(key[0])
                y = int(key[1])
                if self.selected_tile is not None:
                    self.surf.blit(value, ((x * self.tile_size) + offset[0], (y * self.tile_size) + offset[1]))
        else:
            """ Tile grid mode"""
            pixel_size_x = (self.width - 20) / PIXEL_NUMBER
            pixel_size_y = (height - 30 - 20) / PIXEL_NUMBER #remplacer 30 par menu height
            pixel_size = int (min(pixel_size_x, pixel_size_y))
            offset_x = int((self.width - (pixel_size * PIXEL_NUMBER)) / 2)
            offset_y = int((height - (pixel_size * PIXEL_NUMBER) - 30) / 2 + 30) #remplacer 30 par menu height

            self.surf.fill((255, 255, 255)) # Background color

            for x in range(16):
                for y in range(16):
                    pygame.draw.rect(self.surf, self.tile_grid[x][y], (x * pixel_size + offset_x, y * pixel_size + offset_y, pixel_size, pixel_size))

            for x in range(0, (PIXEL_NUMBER + 1) * pixel_size, pixel_size):
                pygame.draw.line(self.surf, (0, 0, 0), (x + offset_x, offset_y), (x + offset_x, pixel_size * PIXEL_NUMBER + offset_y))
                pygame.draw.line(self.surf, (0, 0, 0), (offset_x, x + offset_y), (pixel_size * PIXEL_NUMBER + offset_x, x + offset_y))



    def draw(self, screen):
        """Draw the main screen on the given screen surface"""

        screen.blit(self.surf, (0, 0))

    def click(self, x, y, offset):
        """Handle a click event on the main screen"""

        if self.selected_tile is None:
            return
        print(offset)
        if offset[0] > 0:
            offset = (offset[0] - self.tile_size, offset[1])
        if offset[1] > 0:
            offset = (offset[0], offset[1] - self.tile_size)
        print(offset)
        index = "{}.{}".format(int((x - offset[0])/self.tile_size), int((y - offset[1])/self.tile_size))
        self.coordinates[index] = self.selected_tile
        print (index, offset)

    def set_color(self, x, y, color, screen):
        height = screen.get_height()
        pixel_size_x = (self.width - 20) / PIXEL_NUMBER
        pixel_size_y = (height - 30 - 20) / PIXEL_NUMBER #remplacer 30 par menu height
        pixel_size = int (min(pixel_size_x, pixel_size_y))
        offset_x = int((self.width - (pixel_size * PIXEL_NUMBER)) / 2)
        offset_y = int((height - (pixel_size * PIXEL_NUMBER) - 30) / 2 + 30) #remplacer 30 par menu height
        index_x = int ((x - offset_x)/pixel_size)
        index_y = int ((y - offset_y)/pixel_size)
        if index_x < 0 or index_x > 15 or index_y < 0 or index_y > 15:
            return
        self.tile_grid[index_x][index_y] = color
