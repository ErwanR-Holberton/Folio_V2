import pygame
import os

class animation_class:
    def __init__(self, position, animation_name, scale=64, path="./animations/"):
        self.path = path + animation_name
        self.frame_number = 0
        self.position = position
        self.scale = (scale, scale)

    def draw_next_frame(self, surface):
        frame_names = [f for f in os.listdir(self.path)]
        frame_names.sort()

        self.frame_number += 1
        if self.frame_number >= len(frame_names):
            self.frame_number = 0

        frame = pygame.image.load(self.path + "/" + frame_names[self.frame_number])
        scaled = pygame.transform.scale(frame, self.scale)
        surface.blit(scaled, self.position)

    def get_size(self):
        name = [f for f in os.listdir(self.path)][0]
        image = pygame.image.load(self.path + "/" + name)
        return image.get_size()

    @staticmethod
    def create_win_animations(screen):
        width, height = screen.get_size()
        array = []
        array.append(__class__((25, height - 500 + 30), "Flame1", 500))
        array.append(__class__((width - 525, height - 500 + 30), "Flame1", 500))
        array.append(__class__((400, 200), "Explosion2", 200))
        array.append(__class__((width - 600, 200), "Explosion2", 200))
        return array
