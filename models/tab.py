import pygame
from models.tab_menus import tab_menus_class

class tab_class():
    width = 300
    names = ["un", "deux", "trois"]
    size_name = 50

    def __init__(self, screen):
        self.menu = []
        self.menu.append(tab_menus_class("un", []))
        self.menu.append(tab_menus_class("deux", []))
        self.menu.append(tab_menus_class("trois", []))
        self.calculate(screen)

    def calculate(self, screen):
        font = pygame.font.Font(None, 22) #create default font size 20
        self.surf = pygame.Surface((self.width, screen.get_height()))
        self.surf.fill((250, 250, 250))
        count = 0
        for name in self.names:
            rendered_text = font.render(name, True, (0, 0, 0))
            self.surf.blit(rendered_text, (count, 0))
            count += self.size_name
        for menu in self.menu:
            menu.draw(self.surf)


    def draw(self, screen):
        screen.blit(self.surf, (screen.get_width() - self.width, 0))

