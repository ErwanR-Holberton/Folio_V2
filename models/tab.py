import pygame
from models.tab_menus import tab_menus_class

TILES_PER_LINE = 8

class tab_class():
    width = 320
    size_name = 50

    def __init__(self, screen):

        from functions import get_tile
    
        self.selected_tile = None
        self.selected_tab = 1
        self.menu = []
        tab_menus_class.menu_width += 7
        self.menu.append(tab_menus_class("Tiles", []))
        self.menu.append(tab_menus_class("Tools", []))
        self.menu.append(tab_menus_class("Settings", []))
        self.tiles = []
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
        font = pygame.font.Font(None, 22) #create default font size 20
        self.surf = pygame.Surface((self.width, screen.get_height()))
        self.surf.fill((250, 250, 250))

        if self.selected_tab == 1:
            count = 0
            for tile in self.tiles:
                self.surf.blit(tile, (0 + (count %TILES_PER_LINE) * 40 + 4, tab_menus_class.menu_height + int(count /TILES_PER_LINE) * 40 + 4))
                count += 1
        if self.selected_tab == 2:
            self.surf.fill((250, 0, 250))
        if self.selected_tab == 3:
            self.surf.fill((250, 250, 0))

        for menu in self.menu:
            menu.draw(self.surf)
        self.draw(screen)


    def draw(self, screen):
        screen.blit(self.surf, (screen.get_width() - self.width, 0))

    def click(self, x, y):
        for button in self.menu:
                button.state = 0
                if button.test_click(x, y):
                    if button.name == "Tiles":
                        self.selected_tab = 1
                    if button.name == "Tools":
                        self.selected_tab = 2
                    if button.name == "Settings":
                        self.selected_tab = 3
        index_x = int (x / 40)
        index_y = int ((y - tab_menus_class.menu_height) /40)
        index = index_y * TILES_PER_LINE + index_x
        if index < len(self.tiles):
            self.selected_tile = self.tiles[index_y * TILES_PER_LINE + index_x]
        return self.selected_tile



