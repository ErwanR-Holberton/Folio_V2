#!/usr/bin/env python3
import sys
sys.dont_write_bytecode = True  # prevent __pycache__ creation
import pygame
from pygame.locals import *
import json
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # change the path
from models.map_class import map_class
from models.entities_class import entities_class

pygame.init()                   #initialise pygame library

screen = pygame.display.set_mode((1200,800), pygame.RESIZABLE | pygame.FULLSCREEN) #create the screen

map_name = sys.argv[1]
map = pygame.image.load(map_name)
map_object = map_class("./saves/autosave_map.json")

"""Initialize the game state"""
running = 1
clock = pygame.time.Clock()


entities_class.load_entities()

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
            for entity in entities_class.all:
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

    screen.blit(map, (map_object.offset[0] * 32, map_object.offset[1] * 32))

    for entity in entities_class.all:
        entity.draw(screen)

    for tile in map_object.tiles.keys():
        x, y = tile.split(".")
        x, y = int(x), int(y)
        pygame.draw.rect(screen, (0, 0, 0), (x * 32, y * 32, 32, 32), 1)

    pygame.display.flip() # Refresh the display

pygame.quit()  # Quit Pygame when the game loop exits
