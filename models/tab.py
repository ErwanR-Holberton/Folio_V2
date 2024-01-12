import pygame
from models.tab_menus import tab_menus_class
from functions import load_tiles

TILES_PER_LINE = 8

class tab_class():
    width = 320
    size_name = 50

    def __init__(self, screen):

        from functions import get_tile
    
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
        tab_menus_class.menu_width += 7
        self.menu.append(tab_menus_class("Tiles", []))
        self.menu.append(tab_menus_class("Tools", []))
        self.menu.append(tab_menus_class("Settings", []))
        self.tiles = []
        for tile in load_tiles():
            self.tiles.append(tile)
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
        self.menu[0].state = 1
        self.calculate(screen)

    def calculate(self, screen):
        """"""
        font = pygame.font.Font(None, 22) #create default font size 20
        self.surf = pygame.Surface((self.width, screen.get_height()))
        self.surf.fill((250, 250, 250))

        if self.selected_tab == 1:
            count = 0
            for tile in self.tiles:
                self.surf.blit(tile, (0 + (count %TILES_PER_LINE) * 40 + 4, tab_menus_class.menu_height + int(count /TILES_PER_LINE) * 40 + 4))
                count += 1
        if self.selected_tab == 2:
            x = 0
            for color in self.colors:
                pygame.draw.circle(self.surf, color, (20 + (x % 10) * 30, 50 + int(x / 10) * 30), 10)
                pygame.draw.circle(self.surf, (0, 0, 0), (20 + (x % 10) * 30, 50 + int(x / 10) * 30), 10, 1)
                x += 1
        if self.selected_tab == 3:
            self.surf.fill((250, 250, 0))

        for menu in self.menu:
            menu.draw(self.surf)
        self.draw(screen)


    def draw(self, screen):
        """"""
        screen.blit(self.surf, (screen.get_width() - self.width, 0))

    def click(self, x, y):
        """"""
        for button in self.menu:
                button.state = 0
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
        index_x = int (x / 40)
        index_y = int ((y - tab_menus_class.menu_height) /40)
        index = index_y * TILES_PER_LINE + index_x
        if index < len(self.tiles):
            self.selected_tile = self.tiles[index_y * TILES_PER_LINE + index_x]
        return self.selected_tile



