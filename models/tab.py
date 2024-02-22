import pygame
from utils.functions import load_tiles, create_text_surface
from models.menu_class import menu_class
from models.button_class import button_class
from pygame.locals import *
import math

TILES_PER_LINE = 8

class tab_class():
    """Class representing a tab in the application interface"""

    width = 320
    size_name = 50
    height = 30

    def __init__(self, screen):
        """Initialize the tab class"""

        self.screen = screen
        self.selected_tab = 1
        self.create_list_of_tiles()
        self.menu = menu_class("tab_menu", screen)
        self.menu.create_tab_menu()
        self.create_tool_variables()
        self.create_settings_variables()
        self.selected_color = (255, 255, 255, 0)
        self.reload_user_tiles()

        """Predefined color palette for drawing tools"""
        self.colors = [
            (255, 0, 0),   # Red
            (0, 255, 0),   # Green
            (0, 0, 255),   # Blue
            (255, 255, 0), # Yellow
            (255, 0, 255), # Magenta
            (0, 255, 255), # Cyan
            (128, 128, 128), # Gray
            (255, 165, 0),   # Orange
            (0, 128, 0),     # Dark Green
            (255, 255, 255, 0)   # Transparent
        ]
        for x in range(10):
            self.colors.append((255, 255, 255))
        self.selected_tile = None

        """Set the initial state with the "Tiles" tab selected"""
        self.menu.buttons[0].state = 1
        self.menu.buttons[0].color = (120, 120, 120)
        self.process_tab(screen)

    def create_tool_variables(self):
        self.tools_obj = []
        self.tools_obj.append(button_class("R"))
        self.tools_obj.append(button_class("G"))
        self.tools_obj.append(button_class("B"))
        self.tools_obj.append(button_class("Validate"))
        self.tools_obj[0].set_position(20, 175, 70, 30)
        self.tools_obj[1].set_position(110, 175, 70, 30)
        self.tools_obj[2].set_position(200, 175, 70, 30)
        self.tools_obj[3].set_position(200, 125, 100, 30)

    def create_settings_variables(self):
        self.settings_obj = [
            button_class("Grid Under").set_position(20, 50, 130, 30)
        ]
        self.settings_obj[0].function = self.settings_obj[0].activate_grid

    def process_tab(self, screen):
        """Calculate the appearance of the tab based on the selected tab"""

        """Create a surface for the tab"""
        self.surf = pygame.Surface((self.width, screen.get_height()))
        self.surf.fill((250, 250, 250)) # Fill background color

        if self.selected_tab == 1:
            """Display tiles in the "Tiles" tab"""
            count = 0
            for tile in self.tiles:
                self.surf.blit(tile, ((count %TILES_PER_LINE) * 40 + 4, 30 + int(count /TILES_PER_LINE) * 40 + 4)) #remplacer par height
                count += 1
            for tile in self.user_tiles:
                self.surf.blit(tile, ((count %TILES_PER_LINE) * 40 + 4, 30 + int(count /TILES_PER_LINE) * 40 + 4)) #remplacer par height
                count += 1
        if self.selected_tab == 2:
            """Display color palette in the "Tools" tab"""
            x = 0
            for color in self.colors:
                pygame.draw.circle(self.surf, color, (20 + (x % 10) * 30, 60 + int(x / 10) * 35), 12)
                pygame.draw.circle(self.surf, (0, 0, 0), (20 + (x % 10) * 30, 60 + int(x / 10) * 35), 12, 1)
                x += 1
            for button in self.tools_obj:
                button.draw(self.surf)
            pygame.draw.rect(self.surf, self.selected_color, (10, 125, 180, 30))
            pygame.draw.rect(self.surf, (0, 0, 0), (10, 125, 180, 30), 1)
        if self.selected_tab == 3:
            """Display a yellow background in the "Settings" tab"""
            self.surf.fill((250, 250, 250))
            for button in self.settings_obj:
                button.draw(self.surf)

        """Draw each tab menu"""
        for button in self.menu.buttons:
            button.draw(self.surf)

        pygame.draw.line(self.surf, (150,150,150), (0,0), (0, screen.get_height()))

    def draw(self, screen):
        """Draw the tab on the screen"""

        for button in self.menu.buttons:
            button.draw(self.surf)
        screen.blit(self.surf, (screen.get_width() - self.width, 0))

    def click(self, x, y):
        """Handle a click event on the tab"""

        """Reset the state of all tab menus"""
        click_detected = 0
        for button in self.menu.buttons:
            button.state = 0

            """Check which tab menu is clicked and set the selected tab accordingly"""
            if button.click(x, y):
                click_detected = 1
                if button.label == "Tiles":
                    self.selected_tab = 1
                    self.grid.mode = 0
                    self.grid.allow_process = 1
                if button.label == "Tools":
                    self.selected_tab = 2
                    self.grid.mode = 1
                    self.grid.allow_process = 1
                if button.label == "Settings":
                    self.selected_tab = 3

        if click_detected == 0:
            """Calculate the index of the clicked tile in the "Tiles" tab"""
            if self.selected_tab == 1: # tiles
                index_x = int (x / 40)
                index_y = int ((y - __class__.height) /40)
                index = index_y * TILES_PER_LINE + index_x

                """Update the selected tile based on the clicked tile"""
                if index == 0:
                    self.selected_tile = None
                elif index < len(self.tiles):
                    self.selected_tile = self.tiles[index]
                elif index - len(self.tiles) < len(self.user_tiles):
                    index -= len(self.tiles)
                    self.selected_tile = self.user_tiles[index]

            elif self.selected_tab == 2: # tools
                for i in range(20):
                    center_x = 20 + (i % 10) * 30
                    center_y = 60 + int(i / 10) * 35
                    temp = (x - center_x) ** 2
                    temp2 = (y - center_y) ** 2
                    distance = math.sqrt(temp + temp2)
                    if distance <= 12:
                        self.selected_color = self.colors[i]

                for button in self.tools_obj:
                    button.state = 0
                    if button.label == "":
                        button.label = button.name
                        button.text_surface = create_text_surface(button.label)
                    if button.click(x, y):
                        if button.name == "Validate":
                            if self.selected_color not in self.colors:
                                for i in range(18, 9, -1):
                                    self.colors[i +1] = self.colors[i]
                                self.colors[10] = self.selected_color


            elif self.selected_tab == 3: # settings
                for button in self.settings_obj:
                    button.click(x, y)

        self.process_tab(self.screen)

        return self.selected_tile

    def create_list_of_tiles(self):
        """Duplicate tiles for demonstration purposes
        Load tiles for the "Tiles" tab"""
        from utils.functions import get_tile
        self.tiles = []
        delete_tile = pygame.image.load("base_assets/delete.png")
        delete_tile = pygame.transform.scale(delete_tile, (32, 32))
        self.tiles.append(delete_tile)
        for tile in load_tiles():
            self.tiles.append(tile)

    def handle_key_input(self, key):
        """handle user input to change RGB values"""
        if self.selected_tab == 2:
            if key >= 1073741913 and key <= 1073741922:
                key = (key - 1073741912) % 10
            elif key >= K_0 and key <= K_9:
                key = (key - 48)
            elif key == K_BACKSPACE:
                key = -1
            else:
                return
            for button_index in range(3): #RGB buttons
                if self.tools_obj[button_index].state == 1:
                    self.tools_obj[button_index].edit_label(key)
            self.selected_color = (self.tools_obj[0].label, self.tools_obj[1].label, self.tools_obj[2].label)
            self.selected_color = tuple(int (x) if x.isdigit() else 255 for x in self.selected_color)

    def reload_user_tiles(self):
        """load user tiles"""
        self.user_tiles = load_tiles("./saves/tiles/")
        for index in range(len(self.user_tiles)):
            self.user_tiles[index] = pygame.transform.scale(self.user_tiles[index], (32, 32))
        self.process_tab(self.screen)
