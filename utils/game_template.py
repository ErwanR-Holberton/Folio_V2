#!/usr/bin/env python3
import sys
sys.dont_write_bytecode = True  # prevent __pycache__ creation

import pygame
from pygame.locals import *

import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # change the path because of subprocess

from models.map_class import map_class  # import models after the path change
from models.entities_class import entities_class
from models.events_class import event_class
from models.animation_class import animation_class
from utils.functions import create_text_surface

pygame.init()                   # initialise pygame library

screen = pygame.display.set_mode((1200,800), pygame.RESIZABLE | pygame.FULLSCREEN)  #create the screen

map_name = sys.argv[1]
map = pygame.image.load(map_name)
map_object = map_class("./saves/autosave_map.json")

"""Initialize the game state"""
running = 1
clock = pygame.time.Clock()

win_animations = animation_class.create_win_animations(screen)
loose_animations = animation_class.create_loose_animations(screen)
entities_class.load_entities(map_object.entities)
event_class.entities = entities_class.all
event_class.load_events(map_object.events)

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
    for entity in entities_class.all:
        entity.automove()

    if entities_class.camera_focus is not None:
        a, b = entities_class.camera_focus.position  # get position of the focused entity
        center_x = screen.get_width() // 2
        center_y = screen.get_height() // 2
        cam = entities_class.camera_offset = [center_x - a, center_y - b]
    else:
        cam = entities_class.camera_offset = [0, 0]

    screen.fill((50, 50, 50))  #Fill the screen with a white background


    screen.blit(map, (map_object.offset[0] * 32 + cam[0], map_object.offset[1] * 32 + cam[1]))

    for entity in entities_class.all:  # draws entities
        entity.draw(screen)

    for tile in map_object.tiles.keys():  # draws border around tiles (temporary)
        x, y = tile.split(".")
        x, y = int(x), int(y)
        pygame.draw.rect(screen, (0, 0, 0), (x * 32, y * 32, 32, 32), 1)

    for event in event_class.all:  # draws border around events (temporary)
        x, y = event.position
        pygame.draw.rect(screen, (255, 255, 255), (x * 32, y * 32, 32, 32), 1)

    if event.win:
        rect = screen.get_rect()
        transparent = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
        transparent.fill((50, 50, 50, 200))
        screen.blit(transparent, (0,0))
        message = create_text_surface("VICTORY", 180, (250, 219, 13), "vinque rg.otf")
        position = list(screen.get_rect().center)
        position[0] -= message.get_width()//2
        position[1] -= message.get_height()//2
        screen.blit(message, position)
        for anim in win_animations:
            anim.draw_next_frame(screen)

    if event.loose:
        rect = screen.get_rect()
        transparent = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
        transparent.fill((255, 100, 100, 80))
        screen.blit(transparent, (0,0))
        message = create_text_surface("Defeat", 180, (255, 50, 50), "BloodyCamp.ttf")
        position = list(screen.get_rect().center)
        position[0] -= message.get_width()//2
        position[1] -= message.get_height()//2
        screen.blit(message, position)
        for anim in loose_animations:
            anim.draw_next_frame(screen)

    pygame.display.flip() # Refresh the display

pygame.quit()  # Quit Pygame when the game loop exits
