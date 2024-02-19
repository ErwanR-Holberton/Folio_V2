import pygame
from time import time
from models.tab import *

PIXEL_NUMBER = 16

class main_screen():

    def __init__(self, screen):
        """Initialize the main screen instance"""
        self.selected_tile = None # Currently selected tile
        self.coordinates = {} # Dictionary to store coordinates and corresponding tiles
        self.tile_size = 32 # Size of each tile
        self.mode = 0 # Display mode (0 for map grid, 1 for tile grid)
        self.tile_grid = [[(255, 255, 255, 0) for value in range(16)] for value in range(16)]
        self.offset = (0, 0)
        self.tile_surf = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA) # create a starting surface of tile size
        self.tile_surf.fill((0, 0, 0, 0))
        self.tile_offset = None
        self.screen = screen
        self.allow_process = 1

        self.process_surface(screen) # process the initial grid

    def process_surface(self, screen, offset = None):
        """process one frame of the grid """

        start = pygame.time.get_ticks()
        if offset != None:
            self.offset = offset
        else:
            offset = self.offset
        self.width = screen.get_width() - tab_class.width
        height = screen.get_height()
        if self.width <= 0:
            return
        self.surf = pygame.Surface((self.width, height), pygame.SRCALPHA)

        if self.mode == 0:
            """Map grid mode"""
            self.surf.fill((54, 57, 63)) # Background color
            self.draw_grid(offset, height)
            if self.tile_offset is not None:
                dx, dy = self.tile_offset
            else:
                dx = dy = 0
            self.surf.blit(self.tile_surf, (offset[0] + dx * self.tile_size, offset[1] + dy * self.tile_size))
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
        print ("process_surface time: ", pygame.time.get_ticks()-start)

    def draw_grid(self, offset, height):
        """draw the grid"""

        dx = offset[0] % self.tile_size
        dy = offset[1] % self.tile_size
        for x in range(0, self.width, self.tile_size):
            pygame.draw.line(self.surf, (0, 0, 0), (x + dx, 0), (x + dx, height)) # Vertical grid lines
        for y in range(0, height, self.tile_size):
            pygame.draw.line(self.surf, (0, 0, 0), (0, y + dy), (self.width, y + dy)) # Horizontal grid lines

    def draw(self, screen):
        """Draw the main screen on the given screen surface"""

        screen.blit(self.surf, (0, 0))

    def click(self, x, y, offset):
        """Handle a click event on the main screen"""
        x -= offset[0]
        y -= offset[1]
        if x < 0:
            x -= self.tile_size
        if y < 0:
            y -= self.tile_size
        index_x = int(x/self.tile_size)
        index_y = int(y/self.tile_size)
        index = "{}.{}".format (index_x, index_y)
        if self.selected_tile is None:
            if index in self.coordinates:
                del self.coordinates[index]
            if self.tile_offset is not None:
                for x in range(self.tile_size):
                    for y in range(self.tile_size):
                        self.tile_surf.set_at(((index_x - self.tile_offset[0]) * self.tile_size + x, (index_y - self.tile_offset[1]) * self.tile_size + y), (0, 0, 0, 0))
        else:
            self.coordinates[index] = self.selected_tile
            self.append_surface(index_x, index_y)
        return index

    def append_surface(self, index_x, index_y):
        """"append the background surface with the new tile"""
        size_x = int(self.tile_surf.get_width() /self.tile_size)
        size_y = int(self.tile_surf.get_height() /self.tile_size)
        if self.tile_offset is None:
            self.tile_offset = (index_x, index_y)
        index_x -= self.tile_offset[0]
        index_y -= self.tile_offset[1]
        if index_x >= 0 and size_x > index_x and index_y >= 0 and size_y > index_y:
            self.tile_surf.blit(self.selected_tile, ((index_x) * self.tile_size, (index_y) * self.tile_size))
        else:
            new_size_x = self.tile_surf.get_width()
            new_size_y = self.tile_surf.get_height()
            modified_offset = (0, 0)
            if index_x >= size_x:
                new_size_x = (index_x +1) * self.tile_size
            elif index_x < 0:
                new_size_x -= index_x * self.tile_size
                modified_offset = (modified_offset[0] - index_x, modified_offset[1])
            if index_y >= size_y:
                new_size_y = (index_y +1) * self.tile_size
            elif index_y < 0:
                new_size_y -= index_y * self.tile_size
                modified_offset = (modified_offset[0], modified_offset[1] - index_y)
            self.tile_offset = (self.tile_offset[0] - modified_offset[0], self.tile_offset[1] - modified_offset[1])
            new_surface = pygame.Surface((new_size_x, new_size_y), pygame.SRCALPHA)
            new_surface.fill((255, 0, 0, 0))
            new_surface.blit(self.tile_surf, (modified_offset[0] * self.tile_size, modified_offset[1] * self.tile_size))
            self.tile_surf = new_surface
            self.tile_surf.blit(self.selected_tile, ((index_x + modified_offset[0]) * self.tile_size, (index_y + modified_offset[1]) * self.tile_size))

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
