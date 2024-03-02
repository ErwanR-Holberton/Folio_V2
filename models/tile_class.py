import pygame
from utils.functions import load_json


class tile_class():
    """define a class for the tiles"""
    def __init__(self, name):
        self.properties = self.load_properties(name)
        self.surface = self.load_image(name)

    def load_image(self, name):
        """load a tile"""
        if name[0] == "b":
            folder = "./base_assets/tiles/"
        elif name[0] == "u":
            folder = "./saves/tiles/"
        image = pygame.image.load(folder + name[1:] + ".png")
        return pygame.transform.scale(image, (32, 32))

    def load_properties(self, name):
        """load the properties of a tile"""
        if name[0] == "b":
            folder = "./base_assets/tiles/"
        elif name[0] == "u":
            folder = "./saves/tiles/"

        print(folder + name[1:] + ".json")
        return load_json(folder + name[1:] + ".json")
