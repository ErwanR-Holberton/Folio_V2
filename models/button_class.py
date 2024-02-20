import pygame
import json
from pygame.locals import *
import os
from utils.popups import popup
from utils.functions import create_text_surface

class button_class():
    def __init__(self, label):
        """Initialize class button with name"""

        self.label = label
        self.color = (150, 150, 150)
        self.state = 0
        self.text_surface = create_text_surface(label)
        self.sub_buttons = []
        self.radius_bottom_right = -1
        self.name = label
        self.function = None
        self.function = self.function_1

    def hover(self, x, y):
        """Check if the given coordinates are within the menu area for hover effect"""

        if x < self.rect_value[0] or x > self.rect_value[0] + self.rect_value[2]:
            return False
        if y < self.rect_value[1] or y > self.rect_value[1] + self.rect_value[3]:
            return False
        if self.state != 1:
            self.color = (160, 160, 160)
        return True

    def hover_subbuttons(self, x, y):
        """hover the subbutons"""
        button_hovered = 0
        if self.state != 1:
            self.color = (150, 150, 150)
        else:
            if self.sub_buttons is not None:
                for button in self.sub_buttons:
                    if button.hover(x, y):
                        button_hovered = 1
        if button_hovered:
            return True

    def set_position(self, x, y, width, height):
        """set the position and size of the button and text"""

        self.rect_value = (x, y, width, height)
        text_x = x + int(width/2) - int(self.text_surface.get_width()/2)
        text_y = y + int((height - self.text_surface.get_height())/2)

        self.position_text = (text_x, text_y)

    def draw(self, screen):
        """Draw the menu on the screen"""

        pygame.draw.rect(screen, self.color, self.rect_value, border_bottom_right_radius= self.radius_bottom_right)
        screen.blit(self.text_surface, self.position_text)
        if self.state == 1:
            for button in self.sub_buttons:
                button.draw(screen)

    def click(self, x, y):
        """ Toggle the menu state and update color accordingly"""

        clicked_sub_button = 0
        if self.state == 1 and self.sub_buttons is not None:
            for button in self.sub_buttons:
                if button.click(x, y):
                    clicked_sub_button = 1
                button.state = 0
        hover = self.hover(x, y)
        if hover:
            if self.state == 0:
                self.state = 1
                self.color = (120, 120, 120)
                if self.name == "R" or self.name == "G" or self.name == "B":
                    if self.label.isalpha():
                        self.label = ""
                        self.text_surface = create_text_surface("")
            else:
                self.state = 0
                self.color = (150, 150, 150)
            if self.function is not None:
                self.function()
        if clicked_sub_button:
            return True
        return hover

    def create_sub_buttons(self, sub_buttons):
        """create the subbutons"""
        if sub_buttons is None:
            return
        count = 0
        x, y, w, h = self.rect_value
        for button_name in sub_buttons:
            count += 1
            new = button_class(button_name)
            new.set_position(x, (y + count * h), w, h)
            self.sub_buttons.append(new)

    def edit_label(self, key):
        """edit the label of the button using the user input(key)"""
        if key == -1: # send -1 to erase last letter
            if len(self.label) > 0:
                self.label = self.label[:-1]
        else:
            if len(self.label) > 0:
                if int(self.label) == 0:
                    self.label = ""
            self.label += str(key)
            if int(self.label) > 255:
                self.label = "255"
        self.text_surface = create_text_surface(self.label)
        x, y, width, height = self.rect_value
        self.set_position(x, y, width, height)

    def function_1(self):
        print(self.label, "clicked")

    def save_tile(self):
        """save a tile as a png file"""
        new_tile = pygame.Surface((len(self.grid.tile_grid), len(self.grid.tile_grid)), pygame.SRCALPHA)
        new_tile.fill((0, 0, 0, 0))
        for line in range (len(self.grid.tile_grid)):
            for column in range (len(self.grid.tile_grid[line])):
                new_tile.set_at((column, line), self.grid.tile_grid[column][line])
        name = popup("Please choose a name for the tile:", "Tile save", self.grid, self.tab, self.top)
        if name is not None:
            pygame.image.save(new_tile, "saves/tiles/" + name + ".png")
        self.grid.tab.reload_user_tiles()

    def load_tile(self):
        """loads a tile from a png"""
        name = popup("Please choose a tile to load:", "Tile load", self.grid, self.tab, self.top)
        if name is not None and os.path.exists("./saves/tiles/" + name + ".png"):
            image = pygame.image.load("saves/tiles/" + name + ".png")
            tile = self.grid.tile_grid = []
            for line in range (image.get_height()):
                new_line = []
                for column in range (image.get_width()):
                    new_line.append(image.get_at((line, column)))
                tile.append(new_line)
            self.grid.allow_process = 1

    def save_tile_json(self):
        """saves a tile to a json file"""
        with open ("dump.json", "w") as file:
            json.dump(self.grid.tile_grid, file)

    def load_tile_json(self):
        """loads a tile from a json file"""
        with open ("dump.json", "r") as file:
            self.grid.tile_grid = json.load(file)

    def new_tile(self):
        """creates a new tile"""
        self.grid.tile_grid = [[(0, 0, 0, 0) for x in range(16)] for y in range(16)]
        self.grid.allow_process = 1

    def save_map(self):
        """save a map"""
        name = popup("Please choose a name for the map:", "Map save", self.grid, self.tab, self.top)
        if name is not None:
            pygame.image.save(self.grid.tile_surf, "saves/maps/" + name + ".png")

    def load_map(self):
        """load a map"""
        name = popup("Please choose a map to load:", "Map load", self.grid, self.tab, self.top)
        if name is not None and os.path.exists("./saves/maps/" + name + ".png"):
            self.grid.tile_surf = pygame.image.load("saves/maps/" + name + ".png")
            self.grid.allow_process = 1
            self.grid.tile_offset = (0, 0)

    def new_map(self):
        self.grid.set = None
        self.grid.tile_surf = pygame.Surface((self.grid.tile_size, self.grid.tile_size), pygame.SRCALPHA) # create a starting surface of tile size
        self.grid.tile_surf.fill((0, 0, 0, 0))
        self.grid.allow_process = 1

    def delete_tile(self):
        """delete a tile"""
        name = popup("Please choose a tile to delete:", "Tile delete", self.grid, self.tab, self.top)
        if name is not None and os.path.exists("./saves/tiles/" + name + ".png"):
            os.remove("./saves/tiles/" + name + ".png")

    def delete_map(self):
        """delete a map"""
        name = popup("Please choose a map to delete:", "Map delete", self.grid, self.tab, self.top)
        if name is not None and os.path.exists("./saves/maps/" + name + ".png"):
            os.remove("./saves/maps/" + name + ".png")

    def undo(self):
        if self.grid.mode == 0:
            print(self.grid.undo_index_map, self.grid.history_map)
            self.grid.undo_index_map += 1
            self.grid.tile_surf = self.grid.history_map[self.grid.undo_index_map]
            print ("mode 0")
        elif self.grid.mode == 1:
            for tableau in self.grid.history_tile:
                print("hello", tableau[0][0:3])
            print (len(self.grid.history_tile))
            print (self.grid.tile_grid)
            print(self.grid.undo_index_tile)
            print(self.grid.tile_grid is self.grid.history_tile[self.grid.undo_index_tile])
            self.grid.undo_index_tile += 1
            self.grid.tile_grid = self.grid.history_tile[self.grid.undo_index_tile]
            print ("mode 1")
            print (self.grid.tile_grid)
        self.grid.allow_process = 1
