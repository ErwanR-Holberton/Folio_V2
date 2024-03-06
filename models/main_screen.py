import pygame
from time import time
from models.tab import *
import copy

PIXEL_NUMBER = 16

class main_screen():

    def __init__(self, screen):
        """Initialize the main screen instance"""
        self.grid_status = 1
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
        self.history_tile = []
        self.history_map = []
        self.undo_index_tile = 0
        self.undo_index_map = 0
        self.dragging = 0
        self.old_index = None
        self.save_history_map()
        self.save_history_tile()
        self.entities = []
        self.events = [{"position": [5,5], "type": "walk_on", "target": "players", "area": 1, "action": "move", "dest": [10,10]},
                       {"position": [1, 1], "type": "walk_on", "target": "players", "area": 1, "action": "win"},
                        {"position": [1, 5], "type": "walk_on", "target": "players", "area": 1, "action": "loose"}]
        self.show_entities = 1
        self.show_events = 1


    def process_surface(self, screen, offset = None):
        """process one frame of the grid """

        if offset != None:          # check offset for unitialised value
            self.offset = offset
        else:
            offset = self.offset

        self.width = screen.get_width() - tab_class.width   # update tab size
        height = screen.get_height()
        if self.width <= 0:
            return
        self.surf = pygame.Surface((self.width, height), pygame.SRCALPHA)

        if self.mode == 0:          # Map grid mode

            self.surf.fill((54, 57, 63)) # Background color
            if self.grid_status == 1:           # draw grid under
                self.draw_grid(offset, height)

            if self.tile_offset is not None:
                dx, dy = self.tile_offset
            else:
                dx = dy = 0

            self.surf.blit(self.tile_surf, (offset[0] + dx * self.tile_size, offset[1] + dy * self.tile_size))

            if self.show_entities or self.tab.selected_tab == 5:
                for entity in self.entities:
                    if entity["skin"] is not None:  # draws entity
                        image = pygame.image.load("./saves/tiles/" + entity["skin"] + ".png")
                        scaled_image = pygame.transform.scale(image, (32, 32))
                        self.surf.blit(scaled_image, (offset[0] + (entity["position"][0]) * 32, offset[1] + (entity["position"][1] * 32)))
                    else:  # or red square
                        pygame.draw.rect(self.surf, (255, 0, 0), (offset[0] + (entity["position"][0]) * 32, offset[1] + (entity["position"][1]) * 32, 32, 32))

                    if self.tab.selected_entity == entity:  # draws white square around the selected entity
                        pygame.draw.rect(self.surf, (255, 255, 255), (offset[0] + (entity["position"][0]) * 32, offset[1] + (entity["position"][1]) * 32, 32, 32), 2)

            if self.show_events or self.tab.selected_tab == 6:
                event_icon = pygame.image.load("./base_assets/Event_icon.png")
                for event in self.events:
                    self.surf.blit(event_icon, (offset[0] + (event["position"][0]) * 32, offset[1] + (event["position"][1] * 32)))

                    if self.tab.selected_event == event:  # draws white square around the selected event
                        pygame.draw.rect(self.surf, (255, 255, 255), (offset[0] + (event["position"][0]) * 32, offset[1] + (event["position"][1]) * 32, 32, 32), 2)

            if self.grid_status == 2:           # draw grid over
                self.draw_grid(offset, height)

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
        if x < 0: #remove ghost column
            x -= self.tile_size
        if y < 0: #remove ghost line
            y -= self.tile_size

        index_x = int(x/self.tile_size) # get index from coordinates
        index_y = int(y/self.tile_size)
        index = "{}.{}".format (index_x, index_y)

        if self.old_index != index:
            self.old_index = index
            self.set_tile(index, index_x, index_y)
        return index

    def set_tile(self, index, index_x, index_y):
        if self.selected_tile is None: # None is the value to delete a tile
            if index in self.coordinates: # so we delete it from the list
                del self.coordinates[index]
                self.save_history_map()

            if self.tile_offset is not None:
                for x in range(self.tile_size): #erase pixel by pixel
                    for y in range(self.tile_size):
                        self.tile_surf.set_at(((index_x - self.tile_offset[0]) * self.tile_size + x, (index_y - self.tile_offset[1]) * self.tile_size + y), (0, 0, 0, 0))
        else:   # if we don't erase we place the tile
            width = self.selected_tile.get_width() // 32
            height = self.selected_tile.get_height() // 32

            if width > 1 or height > 1: #handle blueprint
                for x in range(width):
                    for y in range(height):
                        tile = self.selected_tile.subsurface((x * 32, y * 32, 32, 32))
                        self.append_surface(index_x + x, index_y + y, tile)
                self.save_history_map()

            elif index not in self.coordinates or self.coordinates[index] != self.selected_tile:
                self.coordinates[index] = self.selected_tile
                self.append_surface(index_x, index_y, self.selected_tile)
                self.save_history_map()

    def append_surface(self, index_x, index_y, tile):
        """"append the background surface with the new tile"""

        #Calculate the size of the background surface in tiles
        size_x = int(self.tile_surf.get_width() /self.tile_size)
        size_y = int(self.tile_surf.get_height() /self.tile_size)

        if self.tile_offset is None: #adjust the index according to the offset
            self.tile_offset = (index_x, index_y)
        index_x -= self.tile_offset[0]
        index_y -= self.tile_offset[1]

        if index_x >= 0 and size_x > index_x and index_y >= 0 and size_y > index_y:
            #the tile fits so no need to append
            self.tile_surf.blit(tile, ((index_x) * self.tile_size, (index_y) * self.tile_size))
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

            new_surface = pygame.Surface((new_size_x, new_size_y), pygame.SRCALPHA) #create a new background with new size
            new_surface.fill((255, 0, 0, 0))
            new_surface.blit(self.tile_surf, (modified_offset[0] * self.tile_size, modified_offset[1] * self.tile_size))
            self.tile_surf = new_surface
            self.tile_surf.blit(tile, ((index_x + modified_offset[0]) * self.tile_size, (index_y + modified_offset[1]) * self.tile_size))

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
        if self.tile_grid[index_x][index_y] != color:
            self.tile_grid[index_x][index_y] = color
            self.save_history_tile()

    def save_history_map(self):
        """save the history of the map"""
        if self.tile_offset is not None:
            offset_copy = (self.tile_offset[0], self.tile_offset[1])
        else:
            offset_copy = None
        if self.undo_index_map == 0:
            if self.dragging == 2:
                self.history_map[0] = [self.tile_surf.copy(), offset_copy]
            else:
                self.history_map.insert(0, [self.tile_surf.copy(), offset_copy])
        else:
            self.history_map.insert(self.undo_index_map, [self.tile_surf.copy(), offset_copy])
            self.history_map = self.history_map[self.undo_index_map:]
            self.undo_index_map = 0
        if self.dragging == 1:
            self.dragging = 2

    def save_history_tile(self):
        """save the history of the tile"""
        if self.undo_index_tile == 0:
            if self.dragging == 2:
                self.history_tile[0] = copy.deepcopy(self.tile_grid)
            else:
                self.history_tile.insert(0, copy.deepcopy(self.tile_grid))
        else:
            self.history_tile[self.undo_index_tile -1] = copy.deepcopy(self.tile_grid)
            self.history_tile = self.history_tile[self.undo_index_tile -1:]
            self.undo_index_tile = 0
        if self.dragging == 1:
            self.dragging = 2

    def new_entity(self, x, y, offset):
        """creates a new entity when the user clicks on the grid"""
        x -= offset[0]
        y -= offset[1]
        if x < 0: #remove ghost column
            x -= self.tile_size
        if y < 0: #remove ghost line
            y -= self.tile_size

        index_x = int(x/self.tile_size) # get index from coordinates
        index_y = int(y/self.tile_size)

        for entity in self.entities:  # check if click on existing entity
            if entity["position"] == [index_x, index_y]:
                self.tab.selected_entity = entity
                self.allow_process = 1
                return
        new_entity = {"skin": None, "stats": {},"name": "Enter_name", "position": [index_x, index_y] }
        self.entities.append(new_entity)
        self.allow_process = 1

        self.tab.selected_entity = new_entity
        self.tab.process_tab(self.screen)

    def new_event(self, x, y, offset):
        """creates a new event when the user clicks on the grid"""
        x -= offset[0]
        y -= offset[1]
        if x < 0: #remove ghost column
            x -= self.tile_size
        if y < 0: #remove ghost line
            y -= self.tile_size

        index_x = int(x/self.tile_size)  # get index from coordinates
        index_y = int(y/self.tile_size)

        for event in self.events:  # check if click on existing event
            if event["position"] == [index_x, index_y]:
                self.tab.selected_event = event
                self.allow_process = 1
                return
        new_event = {"position": [index_x, index_y], "type": None, "target": "all", "area": 1, "action": None}
        self.events.append(new_event)
        self.allow_process = 1

        self.tab.selected_event = new_event
        self.tab.process_tab(self.screen)



