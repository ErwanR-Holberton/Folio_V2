import pygame
import json
from models.map_class import map_class
from models.events_class import event_class
from random import randint
import os
from utils.functions import list_png, create_text_surface

body_path = "animations/Character/Body/"

class entities_class:
    """define entities class"""

    all = []
    camera_focus = None
    camera_offset = [0, 0]
    def __init__(self, ent_dict):

        self.move_cooldown = 0
        for key, value in ent_dict.items():
            if key == "skin":
                self.icon = self.load_icon(value)
            elif key == "position":
                self.position = [x * 32 for x in value]
            else:
                setattr(self, key, value)
        if "body" in self.animations:
            """self.direction = "down"""
            path = body_path + self.animations["body"]
            if os.path.exists(path):
                skins = list_png(path)
                if "down.png" in skins:
                    self.change_direction("down")
        __class__.camera_focus = self
        __class__.all.append(self)

    def move(self, key):
        """move the entity player"""
        if not hasattr(self, "keys"):
            return

        if "body" in self.animations:
            new_direction = self.direction
        pos = [self.position[0], self.position[1]]

        if key == self.keys[0]:
            pos[1] -= 32
            new_direction = "up"
        elif key == self.keys[1]:
            pos[0] += 32
            new_direction = "right"
        elif key == self.keys[2]:
            pos[1] += 32
            new_direction = "down"
        elif key == self.keys[3]:
            pos[0] -= 32
            new_direction = "left"

        x = pos[0]//32
        y = pos[1]//32

        map = map_class.list_of_maps[map_class.current_map]  # get the current map

        index = "{}.{}".format(x, y)
        if index in map.tiles:  # moves the character only if tile is traversable
            if map.tiles[index].properties["traversable"] == 1:
                self.position = [pos[0], pos[1]]
                if "body" in self.animations:
                    self.change_direction(new_direction)
                for event in event_class.all:
                    if event.type == "walk_on":
                        if event.position == [x, y]:
                            event.trigger(self)

    def automove(self):
        """make the entities move on their own"""
        if self.mobility == 0 or pygame.time.get_ticks() - self.move_cooldown < 500:
            return
        pos = [self.position[0], self.position[1]]

        x = pos[0]//32
        y = pos[1]//32
        direction = self.direction
        if randint(0, 1):
            change = randint(-1, 1)
            x += change
            direction = "right" if change == 1 else ("left" if change == -1 else direction)
        else:
            change = randint(-1, 1)
            y += change
            direction = "down" if change == 1 else ("up" if change == -1 else direction)

        map = map_class.list_of_maps[map_class.current_map]  # get the current map

        index = "{}.{}".format(x, y)
        if self.path_tiles == [] or [x, y] in self.path_tiles:
            if index in map.tiles:  # moves the character only if tile is traversable
                if map.tiles[index].properties["traversable"] == 1:
                    self.position = [x * 32, y * 32]
                    self.change_direction(direction)
                    self.move_cooldown = pygame.time.get_ticks()
                    for event in event_class.all:
                        if event.type == "walk_on":
                            if event.position == [x, y]:
                                event.trigger(self)

    @staticmethod
    def load_entities(entities_list):
        """loads an entity from the list of entities in the map"""
        for dict in entities_list:
            __class__(dict)

    def load_icon(self, path):
        """loads an icon from a string"""
        if path is None:
            return None
        icon = pygame.image.load("./saves/tiles/" + path + ".png")
        return pygame.transform.scale(icon, (32, 32))

    def change_direction(self, direction):
        """change the icon according to direction"""
        self.direction = direction
        path = body_path + self.animations["body"] + "/" + direction + ".png"
        if not os.path.exists(path):
            return
        icon = pygame.image.load(path)
        self.icon = pygame.transform.scale(icon, (32, 32))
        self.add_clothes()

    def add_clothes(self):
        """Adds some layers to the skin if the path exists"""

        base_path = "./animations/Character/"
        direc = self.direction

        if "outfit" in self.animations:
            outfit = self.animations["outfit"]
        else:
            outfit = None
        if "hair" in self.animations:
            hair = self.animations["hair"]
        else:
            hair = None
        if "hat" in self.animations:
            hat = self.animations["hat"]
        else:
            hat = None
        if outfit is not None:
            path = base_path + "Outfit/" + outfit + "/" + direc + ".png"
            if os.path.exists(path):
                outfit = pygame.image.load(path)
                self.icon.blit(outfit, (0, 0))

        if hair is not None:
            path = base_path + "Hair/" + hair + "/" + direc + ".png"
            if os.path.exists(path):
                hair = pygame.image.load(path)
                self.icon.blit(hair, (0, 0))

        if hat is not None:
            path = base_path + "Hat/" + hat + "/" + direc + ".png"
            if os.path.exists(path):
                hat = pygame.image.load(path)
                self.icon.blit(hat, (0, 0))

    def draw(self, screen):
        """draw the entity on the map"""
        if self.icon is None:
            return
        x = self.position[0] + self.camera_offset[0]
        y = self.position[1] + self.camera_offset[1]
        screen.blit(self.icon, [x, y])
