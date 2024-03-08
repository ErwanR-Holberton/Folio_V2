import pygame
import json
from models.map_class import map_class
from models.events_class import event_class
from random import randint

class entities_class:

    all = []
    def __init__(self, ent_dict):

        self.move_cooldown = 0
        for key, value in ent_dict.items():
            if key == "skin":
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

        map = map_class.list_of_maps[map_class.current_map]  # get the current map

        index = "{}.{}".format(x, y)
        if index in map.tiles:  # moves the character only if tile is traversable
            if map.tiles[index].properties["traversable"] == 1:
                self.position = [pos[0], pos[1]]
                for event in event_class.all:
                    if event.type == "walk_on":
                        if event.position == [x, y]:
                            event.trigger(self)

    def automove(self):

        if self.mobility == 0 or pygame.time.get_ticks() - self.move_cooldown < 500:
            return
        pos = [self.position[0], self.position[1]]

        x = pos[0]//32
        y = pos[1]//32
        if randint(0, 1):
            x += randint(-1, 1)
        else:
            y += randint(-1, 1)

        map = map_class.list_of_maps[map_class.current_map]  # get the current map

        index = "{}.{}".format(x, y)
        if index in map.tiles:  # moves the character only if tile is traversable
            if map.tiles[index].properties["traversable"] == 1:
                self.position = [x * 32, y * 32]
                self.move_cooldown = pygame.time.get_ticks()
                for event in event_class.all:
                    if event.type == "walk_on":
                        if event.position == [x, y]:
                            event.trigger(self)

    @staticmethod
    def load_entities():
        """loads an entity from a json file"""
        with open ("./saves/autosave_entities.json", "r") as file:
            entities = json.load(file)
        for dict in entities:
            __class__(dict)

    def load_icon(self, path):
        """loads an icon from a string"""
        if path is None:
            return None
        icon = pygame.image.load("./saves/tiles/" + path + ".png")
        return pygame.transform.scale(icon, (32, 32))

    def draw(self, screen):
        """draw the entity on the map"""
        if self.icon is None:
            return
        screen.blit(self.icon, self.position)
