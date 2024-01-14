import pygame

class submenus_class():
    def __init__(self, name):
        """Initialize submenu instance with a given name"""

        """Create text representation using a default font size of 20"""
        font = pygame.font.Font(None, 20)                           
        self.text = font.render(name, True, (0, 0, 0))

        """Set default color for the submenu"""
        self.color = (150, 150, 150)

