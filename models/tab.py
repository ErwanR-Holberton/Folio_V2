import pygame
from models.tab_menus import tab_menus_class

class tab_class():
    width = 300
    size_name = 50

    def __init__(self, screen):

        from functions import get_tile
    
        self.selected_tab = 1
        self.menu = []
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
                self.surf.blit(tile, (0 + (count %9) * 32, tab_menus_class.menu_height + int(count /9) * 32))
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

