#!/usr/bin/env python3
import pygame
from pygame.locals import *
from drop_down_menu import drop_down_menu
from submenus import submenus_class

pygame.init()   #initialise pygame library ?

screen_info = pygame.display.Info() # Get the screen's width and height
screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), pygame.RESIZABLE) #create the screen
running = 1

list = []
list.append(drop_down_menu("Project", ["New", "Load", "Save"]))
list.append(drop_down_menu("Map", ["New", "Load", "Save"]))
list.append(drop_down_menu("Play", ["This map", "That map"]))
list.append(drop_down_menu("Help", []))

while running:
    for event in pygame.event.get():
        if event.type == QUIT:          #if click on red cross
            running = 0

        elif event.type == KEYDOWN:             #if key is pressed
            if event.key == pygame.K_ESCAPE:
                running = 0

        elif event.type == MOUSEBUTTONUP:
            mouse_x, mouse_y = event.pos
            for menu in list:
                menu.state = 0
                menu.test_click(mouse_x, mouse_y)

        elif event.type == MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            for menu in list:
                if menu.state != 1:
                    if menu.test_hover(mouse_x, mouse_y):
                        menu.color = (160, 160, 160)
                    else:
                        menu.color = (150, 150, 150)


    screen.fill((255, 255, 255))
    
    for menu in list:
        menu.draw(screen)
        if menu.state == 1:
            menu.draw_submenus(screen)

                     
    pygame.display.flip()                               #refresh screen

pygame.quit() # Quit Pygame
