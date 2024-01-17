import pygame
from functions import load_tiles

TILES_PER_LINE = 8

class tab_class():
    """Class representing a tab in the application interface"""

    width = 320
    size_name = 50

    def __init__(self, screen):
        """Initialize the tab class"""

        from functions import get_tile

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
            (128, 0, 128)   # Purple
        ]
        for x in range(10):
            self.colors.append((255, 255, 255))
        self.screen = screen
        self.selected_tile = None
        self.selected_tab = 1
        self.menu = []

        """Adjust the width of the menu based on the number of tabs"""
        #tab_menus_class.menu_width += 7

        """Create tab menus for "Tiles", "Tools", and "Settings"""
        #self.menu.append(tab_menus_class("Tiles", []))
        #self.menu.append(tab_menus_class("Tools", []))
        #self.menu.append(tab_menus_class("Settings", []))

        """Load tiles for the "Tiles" tab"""
        self.tiles = []
        for tile in load_tiles():
            self.tiles.append(tile)

        """Duplicate tiles for demonstration purposes"""
        self.tiles.append(get_tile(37, 26))
        self.tiles.append(get_tile(12, 2))
        self.tiles.append(get_tile(37, 26))
        self.tiles.append(get_tile(12, 2))
        self.tiles.append(get_tile(37, 26))
        self.tiles.append(get_tile(12, 2))
        self.tiles.append(get_tile(37, 26))
        self.tiles.append(get_tile(0, 0))
        self.tiles.append(get_tile(37, 26))
        self.tiles.append(get_tile(12, 2))
        self.tiles.append(get_tile(37, 26))
        self.tiles.append(get_tile(12, 2))
        self.tiles.append(get_tile(37, 26))
        self.tiles.append(get_tile(12, 2))
        self.tiles.append(get_tile(37, 26))
        self.tiles.append(get_tile(12, 2))
        self.tiles.append(get_tile(37, 26))
        self.tiles.append(get_tile(12, 2))
        self.tiles.append(get_tile(37, 26))
        self.tiles.append(get_tile(12, 2))

        """Set the initial state with the "Tiles" tab selected"""
        #self.menu[0].state = 1
        self.calculate(screen)

    def calculate(self, screen):
        """Calculate the appearance of the tab based on the selected tab"""

        font = pygame.font.Font(None, 22) #create default font size 20

        """Create a surface for the tab"""
        self.surf = pygame.Surface((self.width, screen.get_height()))
        self.surf.fill((250, 250, 250)) # Fill background color

        if self.selected_tab == 1:
            """Display tiles in the "Tiles" tab"""
            count = 0
            for tile in self.tiles:
                self.surf.blit(tile, (0 + (count %TILES_PER_LINE) * 40 + 4, 30 + int(count /TILES_PER_LINE) * 40 + 4)) #remplacer par height
                count += 1
        if self.selected_tab == 2:
            """Display color palette in the "Tools" tab"""
            x = 0
            for color in self.colors:
                pygame.draw.circle(self.surf, color, (20 + (x % 10) * 30, 50 + int(x / 10) * 30), 10)
                pygame.draw.circle(self.surf, (0, 0, 0), (20 + (x % 10) * 30, 50 + int(x / 10) * 30), 10, 1)
                x += 1
        if self.selected_tab == 3:
            """Display a yellow background in the "Settings" tab"""
            self.surf.fill((250, 250, 0))

        """Draw each tab menu"""
        for menu in self.menu:
            menu.draw(self.surf)

        """Draw the tab on the screen"""
        self.draw(screen)


    def draw(self, screen):
        """Draw the tab on the screen"""

        screen.blit(self.surf, (screen.get_width() - self.width, 0))

    def click(self, x, y):
        """Handle a click event on the tab"""

        """Reset the state of all tab menus"""
        for button in self.menu:
                button.state = 0

                """Check which tab menu is clicked and set the selected tab accordingly"""
                if button.test_click(x, y):
                    if button.name == "Tiles":
                        self.selected_tab = 1
                        self.grid.mode = 0
                        self.grid.calculate(self.screen)
                    if button.name == "Tools":
                        self.selected_tab = 2
                        self.grid.mode = 1
                        self.grid.calculate(self.screen)
                    if button.name == "Settings":
                        self.selected_tab = 3

        """Calculate the index of the clicked tile in the "Tiles" tab"""
        index_x = int (x / 40)
        index_y = int ((y - 30) /40) #remplacer par height
        index = index_y * TILES_PER_LINE + index_x

        """Update the selected tile based on the clicked tile"""
        if index < len(self.tiles):
            self.selected_tile = self.tiles[index_y * TILES_PER_LINE + index_x]
        return self.selected_tile



