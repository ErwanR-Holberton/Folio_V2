import pygame
from utils.functions import load_json
from models.tab import *
import copy
import os
from uuid import uuid4

PIXEL_NUMBER = 16

class main_screen():

    def __init__(self, screen):
        """Initialize the main screen instance"""

        self.set_variables()

        self.coordinates = {} # Dictionary to store coordinates and corresponding tiles
        self.tile_size = 32 # Size of each tile
        self.mode = 0 # Display mode (0 for map grid, 1 for tile grid)

        # creates empty tile
        self.tile_grid = [[(0, 0, 0, 0) for value in range(16)] for value in range(16)]
        # create a starting surface of tile size
        self.tile_surf = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
        self.tile_surf.fill((0, 0, 0, 0))

        self.screen = screen

        self.save_history_map()  # saves initial empty map
        self.save_history_tile()

    def set_variables(self):
        """set some variables here to clean the init function"""
        self.selected_tile = None # Currently selected tile
        self.allow_process = 1  # allows the main to process this instance to avoid unecessary loops
        self.dragging = 0
        self.old_index = None

        self.offset = (0, 0)  # the amount of pixels
        self.tile_offset = None  # the number of tiles

        self.grid_status = 1

        self.entities = []  # lists of events and entities on the map
        self.events = []
        self.show_entities = 1  # display settings for event and entities
        self.show_events = 1

        self.undo_index_tile = 0  # history variables
        self.undo_index_map = 0
        self.history_tile = []
        self.history_map = []

    def process_surface(self, screen, offset = None):
        """process one frame of the grid """

        if offset != None:          # check offset for unitialised value
            self.offset = offset
        else:
            offset = self.offset

        self.width = screen.get_width() - tab_class.width   # update grid size
        height = screen.get_height()

        if self.width <= 0:
            return

        self.surf = pygame.Surface((self.width, height), pygame.SRCALPHA)

        if self.mode == 0:          # Map mode
            self.process_map_mode(offset, height)
        else:  # tile mode
            self.process_tile_mode(height)

    def process_map_mode(self, offset, height):
        """process the map mode"""

        self.surf.fill((54, 57, 63)) # Background color
        if self.grid_status == 1:           # draw grid under
            self.draw_grid(offset, height)

        if self.tile_offset is not None:
            dx, dy = self.tile_offset
        else:
            dx = dy = 0

        self.surf.blit(self.tile_surf, (offset[0] + dx * self.tile_size, offset[1] + dy * self.tile_size))

        if self.show_entities or self.tab.selected_tab == 5:
            self.draw_entities(offset)

        if self.show_events or self.tab.selected_tab == 6:
            self.draw_events(offset)


        if self.grid_status == 2:           # draw grid over
            self.draw_grid(offset, height)

    def process_tile_mode(self, height):
        """process the tile mode"""
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

    def draw_entities(self, offset):
        """draws all the entities"""
        for entity in self.entities:
            if entity["skin"] is not None:  # draws entity
                image = pygame.image.load("./saves/tiles/" + entity["skin"] + ".png")
                scaled_image = pygame.transform.scale(image, (32, 32))
                self.surf.blit(scaled_image, (offset[0] + (entity["position"][0]) * 32, offset[1] + (entity["position"][1] * 32)))
            else:  # or red square
                pygame.draw.rect(self.surf, (255, 0, 0), (offset[0] + (entity["position"][0]) * 32, offset[1] + (entity["position"][1]) * 32, 32, 32))

            if self.tab.selected_entity == entity:  # draws white square around the selected entity
                pygame.draw.rect(self.surf, (255, 255, 255), (offset[0] + (entity["position"][0]) * 32, offset[1] + (entity["position"][1]) * 32, 32, 32), 2)
                for path_tile in entity["path_tiles"]:
                    pygame.draw.rect(self.surf, (255, 255, 0), (offset[0] + path_tile[0] * 32, offset[1] + path_tile[1] * 32, 32, 32), 1)

    def draw_events(self, offset):
        """draws all events on the grid"""
        event_icon = pygame.image.load("./base_assets/Event_icon.png")

        for event in self.events:
            self.surf.blit(event_icon, (offset[0] + (event["position"][0]) * 32, offset[1] + (event["position"][1] * 32)))

            if self.tab.selected_event == event:  # draws white square around the selected event
                pygame.draw.rect(self.surf, (255, 255, 255), (offset[0] + (event["position"][0]) * 32, offset[1] + (event["position"][1]) * 32, 32, 32), 2)

                if "dest" in event["optional_keys"]:  # if the selected event has dest it draws a green rectangle at destination
                    dest_x, dest_y = event["optional_keys"]["dest"]
                    pygame.draw.rect(self.surf, (0, 255, 0), (offset[0] + dest_x * 32, offset[1] + dest_y * 32, 32, 32), 1)

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
                        button = self.tab.tools_obj[0]  # use a button
                        path = button.get_path_from_img(tile, full=1)  #

                        if path is not None and os.path.exists(path):
                            tile = pygame.image.load(path)
                            tile = pygame.transform.scale(tile, (32, 32))
                            self.coordinates["{}.{}".format(index_x + x, index_y + y)] = tile

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
        if self.undo_index_map == 0:  # did not use ctrl-z before
            if self.dragging == 2:  # overwrite the save if dragging
                self.history_map[0] = [self.tile_surf.copy(), offset_copy, self.coordinates.copy()]
            else:  # new save if not dragging
                self.history_map.insert(0, [self.tile_surf.copy(), offset_copy, self.coordinates.copy()])
        else:  # used ctrl-z before
            self.history_map.insert(self.undo_index_map, [self.tile_surf.copy(), offset_copy, self.coordinates.copy()])
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

    def new_entity(self, x, y):
        """creates a new entity when the user clicks on the grid"""

        if self.mode == 1:
            return

        index_x, index_y = self.calculate_coordinates(x, y)

        for entity in self.entities:  # check if click on existing entity
            if entity["position"] == [index_x, index_y]:
                self.select_entity(entity)
                return

        new_entity = {"id": str(uuid4()), "skin": None, "stats": {},
                      "name": "Enter_name", "position": [index_x, index_y],
                      "path_tiles": [], "mobility": 0, "animation": "Trainer"}

        self.entities.append(new_entity)
        self.select_entity(new_entity)

    def select_entity(self, entity):
        """select an entity and load the dictionnary"""
        self.tab.selected_entity = entity
        if "keys" in entity:
            self.tab.entities_obj[2].change_label("Playable: yes")
        else:
            self.tab.entities_obj[2].change_label("Playable: no")
        if entity["mobility"]:
            self.tab.entities_obj[3].change_label("Mobility: yes")
        else:
            self.tab.entities_obj[3].change_label("Mobility: no")
        self.allow_process = 1
        self.tab.process_tab(self.screen)

    def new_event(self, x, y):
        """creates a new event when the user clicks on the grid"""

        if self.mode == 1:
            return

        index_x, index_y = self.calculate_coordinates(x, y)

        for event in self.events:  # check if click on existing event
            if event["position"] == [index_x, index_y]:
                self.select_event(event)
                return
        new_event = {"position": [index_x, index_y], "type": "walk_on", "target": "one", "area": 1, "action": "move", "optional_keys": {}}
        self.events.append(new_event)
        self.select_event(new_event)

    def select_event(self, event):
        """select an event and change the buttons according to the dictionnary"""
        self.tab.selected_event = event
        self.allow_process = 1
        """button type"""
        index = self.find_index(event["type"], ["walk_on", "map_start"])
        self.tab.events_obj[0].label_number = index - 1
        self.tab.events_obj[0].cycle_labels(["Type: walk on", "Type: map start"])
        """button action"""
        index = self.find_index(event["action"], ["move", "change_stat", "create_entity", "win", "loose"])
        self.tab.events_obj[1].label_number = index - 1
        self.tab.events_obj[1].cycle_labels(["Action: move", "Action: change stat", "Action: create entity", "Action: win", "Action: loose"])
        self.tab.process_tab(self.screen)

    def find_index(self, value, array):
        """find the position of the value in the array"""
        count = 0
        for item in array:
            if value == item:
                return count
            count += 1

    def calculate_coordinates(self, x, y):
        """convert pixel value to tile index"""
        x -= self.offset[0]
        y -= self.offset[1]

        if x < 0: #remove ghost column
            x -= self.tile_size
        if y < 0: #remove ghost line
            y -= self.tile_size

        index_x = int(x/self.tile_size)  # get index from coordinates
        index_y = int(y/self.tile_size)

        return index_x, index_y

    def delete_entity_or_event(self, x, y):
        """delete an entity or an event"""
        if x > self.width:
            return

        index_x, index_y = self.calculate_coordinates(x, y)

        if self.tab.selected_tab == 5:  # entities
            for entity in self.entities:
                if [index_x, index_y] == entity["position"]:
                    if entity == self.tab.selected_entity:
                        self.tab.selected_entity = None
                    self.entities.remove(entity)

        elif self.tab.selected_tab == 6:  # events
            for event in self.events:
                if [index_x, index_y] == event["position"]:
                    if event == self.tab.selected_event:
                        self.tab.selected_event = None
                    self.events.remove(event)
        self.allow_process = 1
        self.tab.process_tab(self.screen)
