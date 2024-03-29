import pygame
import os

class animation_class:
    """define animation class"""
    def __init__(self, position, animation_name, scale=64, path="./animations/"):
        """Initialize the animation object"""
        self.path = path + animation_name
        self.frame_number = 0
        self.position = position
        self.scale = (scale, scale)

    def draw_next_frame(self, surface):
        """Draw the next frame of the animation on the given surface."""
        frame_names = [f for f in os.listdir(self.path)]
        frame_names.sort()

        self.frame_number += 1
        if self.frame_number >= len(frame_names):
            self.frame_number = 0

        frame = pygame.image.load(self.path + "/" + frame_names[self.frame_number])
        scaled = pygame.transform.scale(frame, self.scale)
        surface.blit(scaled, self.position)

    def get_size(self):
        """ Get the size of the first frame of the animation."""
        name = [f for f in os.listdir(self.path)][0]
        image = pygame.image.load(self.path + "/" + name)
        return image.get_size()

    @staticmethod
    def create_win_animations(screen):
        """ Create a list of Animation objects for winning animations."""
        width, height = screen.get_size()
        array = []
        array.append(__class__((25, height - 500 + 30), "Flames/1", 500))
        array.append(__class__((width - 525, height - 500 + 30), "Flames/1", 500))
        array.append(__class__((400, 200), "Explosions/2", 200))
        array.append(__class__((width - 600, 200), "Explosions/2", 200))
        return array

    @staticmethod
    def create_loose_animations(screen):
        """Create a list of Animation objects for losing animations."""
        width, height = screen.get_size()
        array = []
        array.append(__class__((25, height - 300 + 30), "Light outline Skull pack", 200))
        array.append(__class__((width - 225, height - 300 + 30), "Light outline Skull pack", 200))
        array.append(__class__((400, 200), "Explosions/2", 200))
        array.append(__class__((width - 600, 200), "Explosions/2", 200))
        return array
