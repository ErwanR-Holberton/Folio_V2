#!/usr/bin/env python3
import sys
sys.dont_write_bytecode = True  # prevent __pycache__ creation
import pygame
from pygame.locals import *
import json

pygame.init()                   #initialise pygame library

screen = pygame.display.set_mode((1200,800), pygame.RESIZABLE | pygame.FULLSCREEN) #create the screen

map_name = sys.argv[1]
map = pygame.image.load(map_name)

"""Initialize the game state"""
running = 1
clock = pygame.time.Clock()

class entities:

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
        if hasattr(self, "keys"):
            if key == self.keys[0]:
                self.position[1] -= 32
            elif key == self.keys[1]:
                self.position[0] += 32
            elif key == self.keys[2]:
                self.position[1] += 32
            elif key == self.keys[3]:
                self.position[0] -= 32

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

entities.load_entities()

"""Main game loop"""
while running:
    clock.tick(30)

    """Event handling loop"""
    for event in pygame.event.get():
        if event.type == QUIT:  # Check for quit event (click on red cross or press Esc key)
            running = 0

        elif event.type == KEYUP:
            if event.key == K_ESCAPE:
                running = 0
            for entity in entities.all:
                entity.move(event.key)

        elif event.type == KEYDOWN:
            pass

        elif event.type == MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

        elif event.type == MOUSEBUTTONUP:  # Check for mouse button click event
            mouse_x, mouse_y = event.pos

        elif event.type == MOUSEMOTION:  # Check for mouse motion event
            mouse_x, mouse_y = event.pos

        elif event.type == VIDEORESIZE:  # Check for window resize event
            pass

    screen.fill((255, 255, 255))  #Fill the screen with a white background

    screen.blit(map, (0, 0))

    for entity in entities.all:
        entity.draw(screen)

    pygame.display.flip() # Refresh the display

pygame.quit()  # Quit Pygame when the game loop exits
