import pygame

class tab_menu_class():
    width = 300
    def __init__(self, screen):
        self.calculate(screen)
        pass

    def calculate(self, screen):
        self.surf = pygame.Surface((self.width, screen.get_height()))
        self.surf.fill((0, 0, 0))


    def draw(self, screen):
        screen.blit(self.surf, (screen.get_width() - self.width, 0))

