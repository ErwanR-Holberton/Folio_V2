import pygame

class tab_menu_class():
    width = 300
    names = ["un", "deux", "trois"]
    def __init__(self, screen):
        self.calculate(screen)
        font = pygame.font.Font(None, 22) #create default font size 20
        for name in self.names:
            name = font.render(name, True, (0, 0, 0))
        pass

    def calculate(self, screen):
        self.surf = pygame.Surface((self.width, screen.get_height()))
        self.surf.fill((250, 250, 250))


    def draw(self, screen):
        screen.blit(self.surf, (screen.get_width() - self.width, 0))

