import pygame
import json
from models.map_class import map_class

class entities_class:

    all = []
    def __init__(self, ent_dict):

        for key, value in ent_dict.items():
            if key == "icon":
                self.icon = self.load_icon(value)
            elif key == "position":
                self.position = [x * 32 for x in value]
            else:
                setattr(self, key, value)
        __class__.all.append(self)

    def move(self, key):
        """move the entity player"""
        pos = [self.position[0], self.position[1]]

        if hasattr(self, "keys"):
            if key == self.keys[0]:
                pos[1] -= 32
            elif key == self.keys[1]:
                pos[0] += 32
            elif key == self.keys[2]:
                pos[1] += 32
            elif key == self.keys[3]:
                pos[0] -= 32

        x = pos[0]//32
        y = pos[1]//32

        map = map_class.list_of_maps[map_class.current_map]

        index = "{}.{}".format(x, y)
        if index in map.tiles:  # moves the character only if tile is traversable
            if map.tiles[index].properties["traversable"] == 1:
                self.position = [pos[0], pos[1]]

    @staticmethod
    def load_entities():
        """loads an entity from a json file"""
        with open ("./saves/autosave_entities.json", "r") as file:
            entities = json.load(file)
        for dict in entities:
            __class__(dict)

    def load_icon(self, path):
        """loads an icon from a string"""
        icon = pygame.image.load(path)
        return pygame.transform.scale(icon, (32, 32))

    def draw(self, screen):
        """draw the entity on the map"""
        screen.blit(self.icon, self.position)
